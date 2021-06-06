#!/bin/bash

PYTHONPATH=.. ../bin/aca-py start \
   --endpoint http://127.0.0.1:8020 \
   --label faber.agent \
   --inbound-transport http 0.0.0.0 8020 \
   --outbound-transport http \
   --admin 0.0.0.0 8021 \
   --admin-insecure-mode \
   --wallet-type indy \
   --wallet-name faber.agent916333 \
   --wallet-key faber.agent916333 \
   --preserve-exchange-records \
   --auto-provision \
   --genesis-url http://localhost:9000/genesis \
   --trace-target log \
   --trace-tag acapy.events \
   --trace-label faber.agent.trace \
   --auto-ping-connection \
   --auto-respond-messages \
   --auto-accept-invites \
   --auto-accept-requests \
   --auto-respond-credential-proposal \
   --auto-respond-credential-offer \
   --auto-respond-credential-request \
   --auto-store-credential

# set these for full auto
#   --auto-respond-credential-proposal \
#   --auto-respond-credential-offer \
#   --auto-respond-credential-request \
#   --auto-respond-presentation-proposal \
#   --auto-respond-presentation-request \
#   --auto-verify-presentation \
