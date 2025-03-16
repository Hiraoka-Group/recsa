import click

from recsa.pipelines import (
    bondsets_to_assemblies_pipeline,
    concatenate_assemblies_excluding_duplicates_pipeline,
    enum_bond_subsets_pipeline, enumerate_assemblies_pipeline)


@click.command('enumerate-assemblies')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.option(
    '--wip-dir', '-w', type=click.Path(), 
    help='Directory to store intermediate files.')
@click.option(
    '--overwrite', '-o',
    is_flag=True, help='Overwrite output file if it exists.')
@click.option(
    '--verbose', '-v',
    is_flag=True, help='Print verbose output.')
def run_enum_assemblies_pipeline(input, output, wip_dir, overwrite, verbose):
    """Enumerates assemblies.
    
    \b
    Parameters
    ----------
    - INPUT: Path to input file.
    - OUTPUT: Path to output file.

    \b
    Options
    -------
    --wip-dir, -w: Directory to store intermediate files.
    --overwrite, -o: Overwrite output file if it exists.
    --verbose, -v: Print verbose output
    """
    enumerate_assemblies_pipeline(
        input, output,
        wip_dir=wip_dir, overwrite=overwrite, verbose=verbose)


@click.command('concat-assembly-lists')
@click.argument('assemblies', type=click.Path(exists=True), nargs=-1)
@click.argument('component_kinds', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.option(
    '--already-unique-within-files', '-u', is_flag=True,
    help='Whether the assemblies in each file are already unique. If used, the isomorphism checks are skipped for the assemblies within each file.')
@click.option(
    '--start', '-s', type=int, default=0,
    help='Starting index for the reindexing of the assemblies.')
@click.option(
    '--overwrite', '-o', is_flag=True,
    help='Overwrite output file if it exists.')
@click.option(
    '--verbose', '-v', is_flag=True,
    help='Print verbose output.')
def run_concat_assembly_lists_pipeline(
        assemblies, component_kinds, output, already_unique_within_files, 
        start, overwrite, verbose):
    """Concatenates assembly lists.

    \b
    Parameters
    ----------
    - ASSEMBLIES: Paths to input files of assemblies.
    - COMPONENT_KINDS: Path to input file of component kinds.
    - OUTPUT: Path to output file.

    \b
    Options
    -------
    --already-unique-within-files, -u: Whether the assemblies in each file are already unique. If used, the isomorphism checks are skipped for the assemblies within each file.
    --start, -s: Starting index for the reindexing of the assemblies.
    --overwrite, -o: Overwrite output file if it exists.
    --verbose, -v: Print verbose output.
    """
    concatenate_assemblies_excluding_duplicates_pipeline(
        assemblies, component_kinds, output,
        already_unique_within_files=already_unique_within_files,
        start=start, overwrite=overwrite, verbose=verbose)


@click.command('enumerate-bond-subsets')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def run_enum_bond_subsets_pipeline(input, output):
    """Enumerates bond subsets.
    
    \b
    Parameters
    ----------
    - INPUT: Path to input file.
    - OUTPUT: Path to output file.
    """
    enum_bond_subsets_pipeline(input, output)


@click.command('bondsets-to-assemblies')
@click.argument('bondsets', type=click.Path(exists=True))
@click.argument('structure', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def run_bondsets_to_assemblies_pipeline(bondsets, structure, output):
    """Converts bondsets to assemblies.
    
    \b
    Parameters
    ----------
    - BONDSETS: Path to input file of bond subsets.
    - STRUCTURE: Path to input file of structure.
    - OUTPUT: Path to output file.
    """
    bondsets_to_assemblies_pipeline(bondsets, structure, output)
