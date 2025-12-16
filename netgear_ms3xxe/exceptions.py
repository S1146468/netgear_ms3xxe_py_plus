class NetgearAPIError(RuntimeError):
    """Raised when the switch API returns errCode != 0 or protocol violations."""
