from version_1_density_base import main as run_density_base
from version_2_density_optimized import main as run_density_optimized
from version_3_topology_base import main as run_topology_base
from version_4_topology_optimized import main as run_topology_optimized


def main():
    run_density_base()
    run_density_optimized()
    run_topology_base()
    run_topology_optimized()


if __name__ == "__main__":
    main()
