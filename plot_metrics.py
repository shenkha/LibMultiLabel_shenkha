import os
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_metrics(log_dir):
    """Load metrics from log files."""
    metrics_data = {
        'train_loss': [],
        'val_loss': [],
        'val_micro_f1': [],
        'val_rp@5': []
    }
    
    # Load training loss
    train_log_path = os.path.join(log_dir, "train_log.json")
    if os.path.exists(train_log_path):
        with open(train_log_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                # Check for both possible key names
                if 'train_loss_epoch' in data:
                    metrics_data['train_loss'].append(data['train_loss_epoch'])
                elif 'train_log_epoch' in data:
                    metrics_data['train_loss'].append(data['train_log_epoch'])
    
    # Load validation metrics
    val_log_path = os.path.join(log_dir, "val_log.json")
    if os.path.exists(val_log_path):
        with open(val_log_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                if 'Loss' in data:
                    metrics_data['val_loss'].append(data['Loss'])
                if 'Micro-F1' in data:
                    metrics_data['val_micro_f1'].append(data['Micro-F1'])
                if 'RP@5' in data:
                    metrics_data['val_rp@5'].append(data['RP@5'])
    
    return metrics_data

def plot_comparison(metrics_dict, output_dir):
    """Plot and compare metrics."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    epochs = range(1, len(list(metrics_dict.values())[0]['train_loss']) + 1)
    
    # Plot Training Loss
    plt.figure(figsize=(10, 6))
    for name, metrics in metrics_dict.items():
        plt.plot(epochs, metrics['train_loss'], label=name)
    plt.title('Training Loss vs. Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'training_loss.png'))
    plt.close()
    
    # Plot Validation Loss
    plt.figure(figsize=(10, 6))
    for name, metrics in metrics_dict.items():
        plt.plot(epochs[:len(metrics['val_loss'])], metrics['val_loss'], label=name)
    plt.title('Validation Loss vs. Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'validation_loss.png'))
    plt.close()
    
    # Plot Micro-F1
    plt.figure(figsize=(10, 6))
    for name, metrics in metrics_dict.items():
        plt.plot(epochs[:len(metrics['val_micro_f1'])], metrics['val_micro_f1'], label=name)
    plt.title('Validation Micro-F1 vs. Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Micro-F1')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'micro_f1.png'))
    plt.close()
    
    # Plot RP@5
    plt.figure(figsize=(10, 6))
    for name, metrics in metrics_dict.items():
        plt.plot(epochs[:len(metrics['val_rp@5'])], metrics['val_rp@5'], label=name)
    plt.title('Validation RP@5 vs. Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('RP@5')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'rp_at_5.png'))
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot metrics from different optimizer experiments')
    parser.add_argument('--log_dirs', nargs='+', required=True, help='Directories containing log files')
    parser.add_argument('--names', nargs='+', required=True, help='Names for each experiment')
    parser.add_argument('--output_dir', default='plots', help='Directory to save plots')
    
    args = parser.parse_args()
    
    if len(args.log_dirs) != len(args.names):
        print("Error: Number of log directories must match number of experiment names")
        exit(1)
    
    # Load metrics for each experiment
    all_metrics = {}
    for log_dir, name in zip(args.log_dirs, args.names):
        all_metrics[name] = load_metrics(log_dir)
    
    # Plot comparison
    plot_comparison(all_metrics, args.output_dir)
    print(f"Plots saved to {args.output_dir}")
