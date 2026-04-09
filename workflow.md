1. PROBE (every 2s)
      ICMP + UDP → end-to-end loss %
   
2. DETECT (30s rolling window)
    Loss >2% → trigger localization
      Log timestamp/context
   
3. LOCALIZE (MTR every 30s on alert)
    Per-hop loss stats
     Flag first hop >5% + final >1%
       Store path snapshot
   
4. SUGGEST (rule-based)
    "Local WiFi issue" → hop 1-2
      "ISP problem" → hop 3+
       "Target issue" → final hop only

   Environment considerations: Package loss is built into the hardware account for.
   wired,

   wireless,

   unknown.
