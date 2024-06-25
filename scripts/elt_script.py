import os
import subprocess
import time

def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Successfully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            print(f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting.")
    return False

def get_db_config(prefix):
    """Get database configuration from environment variables."""
    return {
        'dbname': os.getenv(f'{prefix}_DB_NAME'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv(f'{prefix}_DB_HOST')
    }

def run_subprocess(command, env):
    """Run a subprocess command with specified environment variables."""
    try:
        subprocess.run(command, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command '{' '.join(command)}' failed with error: {e}")
        exit(1)

def dump_database(config, output_file):
    """Dump the source database to a SQL file."""
    command = [
        'pg_dump',
        '-h', config['host'],
        '-U', config['user'],
        '-d', config['dbname'],
        '-f', output_file,
        '-w'  # Do not prompt for password
    ]
    env = {'PGPASSWORD': config['password']}
    run_subprocess(command, env)

def load_database(config, input_file):
    """Load the dumped SQL file into the destination database."""
    command = [
        'psql',
        '-h', config['host'],
        '-U', config['user'],
        '-d', config['dbname'],
        '-a', '-f', input_file
    ]
    env = {'PGPASSWORD': config['password']}
    run_subprocess(command, env)

def main():
    # Wait for source PostgreSQL to be available
    if not wait_for_postgres(host=os.getenv('SOURCE_DB_HOST')):
        exit(1)

    # Wait for destination PostgreSQL to be available
    if not wait_for_postgres(host=os.getenv('DESTINATION_DB_HOST')):
        exit(1)

    print("Starting ELT script...")

    # Get database configurations
    source_config = get_db_config('SOURCE')
    destination_config = get_db_config('DESTINATION')

    # Dump the source database to a SQL file
    dump_database(source_config, 'data_dump.sql')

    # Load the dumped SQL file into the destination database
    load_database(destination_config, 'data_dump.sql')

    print("Ending ELT script...")

if __name__ == '__main__':
    main()
