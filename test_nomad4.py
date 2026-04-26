# Wait, if "No allocations placed" is returned, it's definitely because the user ran it without the TLS certs, or on the wrong namespace, or the allocs were garbage collected.
# I should tell the user to source the profile script and run `nomad job allocs -all authentik`.
