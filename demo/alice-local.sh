#!/bin/bash

PYTHONPATH=.. ../bin/aca-py start \
   --endpoint http://127.0.0.1:8030 \
   --label alice.agent \
   --inbound-transport http 0.0.0.0 8030 \
   --outbound-transport http \
   --admin 0.0.0.0 8031 \
   --admin-insecure-mode \
   --wallet-type indy \
   --wallet-name alice.agent420695 \
   --wallet-key alice.agent420695 \
   --preserve-exchange-records \
   --auto-provision \
   --genesis-url http://localhost:9000/genesis \
   --trace-target log \
   --trace-tag acapy.events \
   --trace-label alice.agent.trace \
   --auto-ping-connection \
   --auto-respond-messages \
   --auto-accept-invites \
   --auto-accept-requests \
   --auto-respond-credential-proposal \
   --auto-respond-credential-offer \
   --auto-respond-credential-request \
   --auto-store-credential \
   --auto-respond-presentation-proposal \
   --auto-respond-presentation-request \
   --auto-verify-presentation
