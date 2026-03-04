import os
import winsound

def trigger_alert(node_id):
    print(f"🚨 EMERGENCY FROM {node_id}")
    winsound.Beep(1000, 1000)
