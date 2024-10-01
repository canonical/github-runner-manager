# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Package containing modules with type definitions."""
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel, Field, IPvAnyAddress, model_validator


class ProxyConfig(BaseModel):
    """Proxy configuration.

    Attributes:
        aproxy_address: The address of aproxy snap instance if use_aproxy is enabled.
        http: HTTP proxy address string.
        http_url: HTTP proxy address url.
        https: HTTPS proxy address string.
        https_url: HTTPS proxy address url.
        no_proxy: Comma-separated list of hosts that should not be proxied.
        use_aproxy: Whether aproxy should be used for the runners.
    """

    http_url: Optional[AnyHttpUrl] = None
    https_url: Optional[AnyHttpUrl] = None
    no_proxy: Optional[str] = None
    use_aproxy: bool = False

    @property
    def http(self) -> Optional[str]:
        """Return string version of http url."""
        return str(self.http_url) if self.http_url else None

    @property
    def https(self) -> Optional[str]:
        """Return string version of https url."""
        return str(self.https_url) if self.https_url else None

    @property
    def aproxy_address(self) -> Optional[str]:
        """Return the aproxy address."""
        if self.use_aproxy:
            proxy_address = self.http_url or self.https_url
            # assert is only used to make mypy happy
            assert (
                proxy_address is not None and proxy_address.host is not None
            )  # nosec for [B101:assert_used]
            aproxy_address = (
                proxy_address.host
                if not proxy_address.port
                else f"{proxy_address.host}:{proxy_address.port}"
            )
        else:
            aproxy_address = None
        return aproxy_address

    @model_validator(mode="after")
    def check_use_aproxy(self: "ProxyConfig") -> "ProxyConfig":
        """Validate the proxy configuration.

        Raises:
            ValueError: if use_aproxy was set but no http/https was passed.

        Returns:
            Validated ProxyConfig instance.
        """
        if self.use_aproxy and not (self.http_url or self.https_url):
            raise ValueError("aproxy requires http or https to be set")

        return self

    def __bool__(self) -> bool:
        """Return whether the proxy config is set.

        Returns:
            Whether the proxy config is set.
        """
        return bool(self.http_url or self.https_url)


class SSHDebugConnection(BaseModel):
    """SSH connection information for debug workflow.

    Attributes:
        host: The SSH relay server host IP address inside the VPN.
        port: The SSH relay server port.
        rsa_fingerprint: The host SSH server public RSA key fingerprint.
        ed25519_fingerprint: The host SSH server public ed25519 key fingerprint.
    """

    host: IPvAnyAddress
    port: int = Field(0, gt=0, le=65535)
    rsa_fingerprint: str = Field(pattern="^SHA256:.*")
    ed25519_fingerprint: str = Field(pattern="^SHA256:.*")


class RepoPolicyComplianceConfig(BaseModel):
    """Configuration for the repo policy compliance service.

    Attributes:
        token: Token for the repo policy compliance service.
        url: URL of the repo policy compliance service.
    """

    token: str
    url: AnyHttpUrl
