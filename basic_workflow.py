#!/usr/bin/env python3
"""
Basic ROW Risk Assessment Workflow Example
==========================================

This example demonstrates how to use the ROW Risk Management System
to perform a complete risk assessment on a power transmission corridor.

Usage:
    python basic_workflow.py --corridor path/to/corridor.shp --output results/
"""

import argparse
import os
from pathlib import Path
import logging

import geopandas as gpd
from loguru import logger

# Import the main assessment class
from row_risk_manager import ROWRiskAssessment
from row_risk_manager.utils import setup_logging, create_sample_data


def main():
    """Main workflow execution."""
    parser = argparse.ArgumentParser(
        description='Run basic ROW risk assessment workflow'
    )
    parser.add_argument(
        '--corridor', 
        type=str,
        help='Path to ROW corridor shapefile or geojson'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='configs/default_config.json',
        help='Configuration file path'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output/',
        help='Output directory for results'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run with demo data (creates sample corridor)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(level=log_level)
    
    logger.info("Starting ROW Risk Assessment Workflow")
    logger.info(f"Configuration: {args.config}")
    logger.info(f"Output directory: {args.output}")
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle demo mode or load actual corridor data
    if args.demo:
        logger.info("Creating demo corridor data...")
        corridor_path = create_sample_corridor_data(output_dir / "demo_corridor.geojson")
    else:
        if not args.corridor:
            logger.error("Corridor path required when not using demo mode")
            return 1
        corridor_path = args.corridor
        
    if not os.path.exists(corridor_path):
        logger.error(f"Corridor file not found: {corridor_path}")
        return 1
    
    # Load and validate corridor data
    try:
        corridor_gdf = gpd.read_file(corridor_path)
        logger.info(f"Loaded corridor with {len(corridor_gdf)} segments")
        
        # Basic validation
        if corridor_gdf.empty:
            raise ValueError("Corridor data is empty")
        if corridor_gdf.crs is None:
            logger.warning("No CRS specified, assuming EPSG:4326")
            corridor_gdf.crs = "EPSG:4326"
            
    except Exception as e:
        logger.error(f"Failed to load corridor data: {e}")
        return 1
    
    # Initialize the ROW Risk Assessment system
    try:
        logger.info("Initializing ROW Risk Assessment system...")
        assessment = ROWRiskAssessment(
            row_corridor_path=corridor_path,
            config_file=args.config
        )
        
        # Run the complete workflow
        logger.info("Starting 5-stage risk assessment workflow...")
        results = assessment.run_full_workflow()
        
        # Save results
        logger.info("Saving results...")
        
        # Save risk data
        if results.get('risk') is not None:
            risk_output = output_dir / "risk_assessment.json"
            save_risk_results(results['risk'], risk_output)
        
        # Save vegetation analysis
        if results.get('vegetation') is not None:
            veg_output = output_dir / "vegetation_analysis.json"
            save_vegetation_results(results['vegetation'], veg_output)
        
        # Save prioritization results
        if results.get('priorities') is not None:
            priority_output = output_dir / "maintenance_priorities.json"
            save_priority_results(results['priorities'], priority_output)
        
        # Generate interactive map if reporting results available
        if results.get('reports') is not None:
            map_output = output_dir / "risk_map.html"
            save_interactive_map(results['reports'].get('map'), map_output)
        
        logger.success("Workflow completed successfully!")
        logger.info(f"Results saved to: {output_dir}")
        
        # Print summary
        print_workflow_summary(results, output_dir)
        
        return 0
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def create_sample_corridor_data(output_path: Path) -> str:
    """Create sample corridor data for demonstration."""
    from shapely.geometry import LineString
    import numpy as np
    
    logger.info("Creating sample transmission line corridor...")
    
    # Create a sample transmission line corridor
    # Simple line from point A to point B with some curves
    coords = [
        (-122.4194, 37.7749),  # San Francisco
        (-122.4094, 37.7849),
        (-122.3994, 37.7949),
        (-122.3894, 37.8049),
        (-122.3794, 37.8149)   # Roughly towards Oakland
    ]
    
    line_geom = LineString(coords)
    
    # Create GeoDataFrame
    corridor_gdf = gpd.GeoDataFrame({
        'line_id': ['DEMO_LINE_001'],
        'line_name': ['Demo Transmission Line'],
        'voltage_kv': [500],
        'owner': ['Demo Utility Company'],
        'in_service_date': ['2020-01-01'],
        'length_km': [line_geom.length * 111.32],  # Rough conversion to km
        'geometry': [line_geom]
    }, crs='EPSG:4326')
    
    # Save to file
    corridor_gdf.to_file(output_path, driver='GeoJSON')
    logger.info(f"Sample corridor saved to: {output_path}")
    
    return str(output_path)


def save_risk_results(risk_data, output_path: Path):
    """Save risk assessment results."""
    import json
    import numpy as np
    
    # Convert numpy arrays to lists for JSON serialization
    serializable_data = convert_numpy_to_json(risk_data)
    
    with open(output_path, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    
    logger.info(f"Risk results saved to: {output_path}")


def save_vegetation_results(veg_data, output_path: Path):
    """Save vegetation analysis results."""
    import json
    
    serializable_data = convert_numpy_to_json(veg_data)
    
    with open(output_path, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    
    logger.info(f"Vegetation results saved to: {output_path}")


def save_priority_results(priority_data, output_path: Path):
    """Save prioritization results."""
    import json
    
    serializable_data = convert_numpy_to_json(priority_data)
    
    with open(output_path, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    
    logger.info(f"Priority results saved to: {output_path}")


def save_interactive_map(map_obj, output_path: Path):
    """Save interactive map if available."""
    if map_obj is not None:
        if hasattr(map_obj, 'save'):
            map_obj.save(str(output_path))
            logger.info(f"Interactive map saved to: {output_path}")
        else:
            logger.warning("Map object doesn't support save method")
    else:
        logger.warning("No map object to save")


def convert_numpy_to_json(obj):
    """Convert numpy arrays to JSON-serializable format."""
    import numpy as np
    
    if isinstance(obj, dict):
        return {k: convert_numpy_to_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_json(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    else:
        return obj


def print_workflow_summary(results, output_dir):
    """Print a summary of the workflow results."""
    print("\n" + "="*60)
    print("ROW RISK ASSESSMENT WORKFLOW SUMMARY")
    print("="*60)
    
    if 'data' in results:
        print("✓ Data Acquisition: Completed")
        
    if 'vegetation' in results:
        print("✓ Vegetation Analysis: Completed")
        
    if 'risk' in results:
        print("✓ Risk Assessment: Completed")
        
    if 'priorities' in results:
        print("✓ Prioritization: Completed")
        
    if 'reports' in results:
        print("✓ Reporting: Completed")
    
    print(f"\nResults Location: {output_dir}")
    print("\nGenerated Files:")
    
    for file_path in output_dir.glob("*"):
        if file_path.is_file():
            print(f"  - {file_path.name}")
    
    print("\nNext Steps:")
    print("  1. Review the interactive risk map (risk_map.html)")
    print("  2. Check maintenance priorities (maintenance_priorities.json)")
    print("  3. Implement high-priority maintenance actions")
    print("  4. Schedule regular monitoring updates")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    exit(main())