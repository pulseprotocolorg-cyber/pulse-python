"""PULSE Protocol TLS transport layer.

This module provides:
- TLS configuration for PulseServer (HTTPS)
- Self-signed certificate generation for development/testing
- TLS context factory with secure defaults (TLS 1.2+)
- Certificate utilities for production deployments

Security Layer 1 of the PULSE 7-layer security model.

Example:
    >>> # Generate dev certificates
    >>> cert_path, key_path = generate_self_signed_cert()

    >>> # Create TLS-enabled server
    >>> tls_config = TLSConfig(certfile=cert_path, keyfile=key_path)
    >>> server = PulseServer(port=8443, tls=tls_config)
    >>> server.start()

    >>> # Connect with client
    >>> client = PulseClient("https://localhost:8443", verify_ssl=False)
"""
import os
import ssl
import tempfile
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class TLSConfig:
    """
    TLS configuration for PULSE server and client.

    Encapsulates all TLS-related settings including certificate paths,
    key files, CA certificates, and protocol version requirements.

    Attributes:
        certfile: Path to PEM-encoded server certificate
        keyfile: Path to PEM-encoded private key
        cafile: Path to CA certificate bundle for client verification
        require_client_cert: Whether to require client certificates (mTLS)
        min_version: Minimum TLS version (default TLS 1.2)
        ciphers: Allowed cipher suites (None = secure defaults)

    Example:
        >>> # Basic server TLS
        >>> config = TLSConfig(
        ...     certfile="/path/to/cert.pem",
        ...     keyfile="/path/to/key.pem"
        ... )

        >>> # Mutual TLS (mTLS)
        >>> config = TLSConfig(
        ...     certfile="/path/to/cert.pem",
        ...     keyfile="/path/to/key.pem",
        ...     cafile="/path/to/ca.pem",
        ...     require_client_cert=True
        ... )
    """

    certfile: str = ""
    keyfile: str = ""
    cafile: Optional[str] = None
    require_client_cert: bool = False
    min_version: int = field(default_factory=lambda: ssl.TLSVersion.TLSv1_2)
    ciphers: Optional[str] = None

    def create_server_context(self) -> ssl.SSLContext:
        """
        Create SSL context for server-side TLS.

        Configures the context with the certificate, key, and security
        settings specified in this TLSConfig.

        Returns:
            Configured SSLContext for server use

        Raises:
            FileNotFoundError: If certificate or key file doesn't exist
            ssl.SSLError: If certificate/key is invalid

        Example:
            >>> config = TLSConfig(certfile="cert.pem", keyfile="key.pem")
            >>> ctx = config.create_server_context()
        """
        if not self.certfile:
            raise ValueError("certfile is required for TLS server")
        if not self.keyfile:
            raise ValueError("keyfile is required for TLS server")

        if not os.path.isfile(self.certfile):
            raise FileNotFoundError(f"Certificate file not found: {self.certfile}")
        if not os.path.isfile(self.keyfile):
            raise FileNotFoundError(f"Key file not found: {self.keyfile}")

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = self.min_version
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)

        if self.cafile:
            if not os.path.isfile(self.cafile):
                raise FileNotFoundError(f"CA file not found: {self.cafile}")
            context.load_verify_locations(cafile=self.cafile)

        if self.require_client_cert:
            context.verify_mode = ssl.CERT_REQUIRED
        else:
            context.verify_mode = ssl.CERT_NONE

        if self.ciphers:
            context.set_ciphers(self.ciphers)

        return context

    def create_client_context(
        self,
        verify: bool = True,
        client_certfile: Optional[str] = None,
        client_keyfile: Optional[str] = None,
    ) -> ssl.SSLContext:
        """
        Create SSL context for client-side TLS.

        Args:
            verify: Whether to verify server certificate (default True)
            client_certfile: Path to client certificate for mTLS
            client_keyfile: Path to client private key for mTLS

        Returns:
            Configured SSLContext for client use

        Example:
            >>> config = TLSConfig(cafile="/path/to/ca.pem")
            >>> ctx = config.create_client_context()

            >>> # mTLS client
            >>> ctx = config.create_client_context(
            ...     client_certfile="client.pem",
            ...     client_keyfile="client-key.pem"
            ... )
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = self.min_version

        if verify:
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            if self.cafile:
                context.load_verify_locations(cafile=self.cafile)
            else:
                context.load_default_certs()
        else:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        if client_certfile and client_keyfile:
            context.load_cert_chain(
                certfile=client_certfile, keyfile=client_keyfile
            )

        if self.ciphers:
            context.set_ciphers(self.ciphers)

        return context


def generate_self_signed_cert(
    hostname: str = "localhost",
    org_name: str = "PULSE Protocol Dev",
    days_valid: int = 365,
    output_dir: Optional[str] = None,
    key_size: int = 2048,
) -> tuple:
    """
    Generate a self-signed certificate for development/testing.

    Uses the cryptography library if available, otherwise falls back
    to OpenSSL command-line tool.

    Args:
        hostname: Certificate common name / SAN (default "localhost")
        org_name: Organization name in certificate subject
        days_valid: Certificate validity in days (default 365)
        output_dir: Directory for cert files (default temp dir)
        key_size: RSA key size in bits (default 2048)

    Returns:
        Tuple of (cert_path, key_path) - absolute paths to generated files

    Raises:
        RuntimeError: If neither cryptography library nor openssl is available

    Example:
        >>> cert_path, key_path = generate_self_signed_cert()
        >>> print(f"Certificate: {cert_path}")
        >>> print(f"Key: {key_path}")

        >>> # Custom hostname
        >>> cert_path, key_path = generate_self_signed_cert(
        ...     hostname="agent.example.com",
        ...     output_dir="/etc/pulse/certs"
        ... )
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="pulse_tls_")
    else:
        os.makedirs(output_dir, exist_ok=True)

    cert_path = os.path.join(output_dir, "cert.pem")
    key_path = os.path.join(output_dir, "key.pem")

    # Try cryptography library first
    try:
        return _generate_with_cryptography(
            hostname, org_name, days_valid, cert_path, key_path, key_size
        )
    except ImportError:
        pass

    # Fallback to openssl command
    return _generate_with_openssl(
        hostname, org_name, days_valid, cert_path, key_path, key_size
    )


def _generate_with_cryptography(
    hostname: str,
    org_name: str,
    days_valid: int,
    cert_path: str,
    key_path: str,
    key_size: int,
) -> tuple:
    """Generate cert using the cryptography library."""
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from datetime import datetime, timedelta, timezone
    import ipaddress

    # Generate key
    key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)

    # Build certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
        x509.NameAttribute(NameOID.COMMON_NAME, hostname),
    ])

    # Subject Alternative Names
    san_list = [x509.DNSName(hostname)]
    if hostname == "localhost":
        san_list.append(x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")))
        san_list.append(x509.IPAddress(ipaddress.IPv6Address("::1")))

    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=days_valid))
        .add_extension(
            x509.SubjectAlternativeName(san_list),
            critical=False,
        )
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=0),
            critical=True,
        )
        .sign(key, hashes.SHA256())
    )

    # Write certificate
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    # Write private key
    with open(key_path, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    return cert_path, key_path


def _generate_with_openssl(
    hostname: str,
    org_name: str,
    days_valid: int,
    cert_path: str,
    key_path: str,
    key_size: int,
) -> tuple:
    """Generate cert using openssl command-line tool."""
    import subprocess

    subject = f"/O={org_name}/CN={hostname}"
    cmd = [
        "openssl", "req", "-x509", "-newkey", f"rsa:{key_size}",
        "-keyout", key_path,
        "-out", cert_path,
        "-days", str(days_valid),
        "-nodes",
        "-subj", subject,
        "-addext", f"subjectAltName=DNS:{hostname},IP:127.0.0.1",
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"openssl failed: {result.stderr}"
            )
        return cert_path, key_path
    except FileNotFoundError:
        raise RuntimeError(
            "Neither 'cryptography' library nor 'openssl' command available. "
            "Install cryptography: pip install cryptography"
        )
