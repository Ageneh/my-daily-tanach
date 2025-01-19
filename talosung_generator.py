from talosung_gen.losungen_csv_generator import run as run_csv_generator
from talosung_gen.losungen_processor import run as run_merge
from talosung_gen.talosung_to_supabase_transformer import run as run_to_supabase
from talosung_gen.preconditions import parse_args

parse_args()

def generate():
    run_csv_generator()
    run_merge()
    run_to_supabase()
    return

if __name__ == '__main__':
    generate()
