from typing import List, Dict

def analyze_path(hops: List[Dict]) -> Dict:
   if not hops:
      return {'status': 'error', 'message': 'No hops data to analyze'}
   
   analysis = {
      'total_hops': len(hops),
      'total_loss': sum(hop['loss'] for hop in hops) / len(hops),
      'average_latency': sum(hop['avg'] for hop in hops) / len(hops),
      'worst_latency': max(hop['worst'] for hop in hops),
      'bottleneck': None
   }

   bottleneck = max(hops, key=lambda x: x['loss'])
   analysis['bottleneck'] = {
      'hop': bottleneck['hop'],
      'host': bottleneck['host'],
      'loss': bottleneck['loss'],
      'avg_latency': bottleneck['avg']
   }

   if analysis['bottleneck']['loss'] > 20:
      analysis['suggestion'] = f"Contact ISP about Hop {bottleneck['hop']} ({bottleneck['host']})"
   else:
      analysis['suggestion'] = 'Path healthy'
   return analysis