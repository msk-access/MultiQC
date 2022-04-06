#!/usr/bin/env python

""" MultiQC submodule to parse output from fgbio CollectDuplexSeqMetrics """

from multiqc.plots import linegraph


def parse_reports(self):
    """Parser metric files for fgbio CollectDuplexSeqMetrics.

    Stores the family_sizes.txt and duplex_yield_metrics.txt metrics into a data file and adds a section
    with a per-sample plot.
    """

    # slurp in all the data
    family_sizes_data = parse_family_sizes(self)
    duplex_yield_metrics_data = parse_duplex_yield_metrics(self)

    # Plot the data and add section
    pconfig_simplex_family_size = {
        "id": "fgbio_CollectDuplexSeqMetrics_simplex_family_sizes",
        "title": "Fgbio: Frequency of simplex family sizes",
        "ylab": "Count",
        "xlab": "Simplex family size",
        "xDecimals": False,
        "tt_label": "<b>family size {point.x}</b>: {point.y}",
        "data_labels": [
            {"name": "Count", "ylab": "Count"},
            {"name": "Fraction", "ylab": "Fraction"},
        ],
    }

    pconfig_duplex_family_size = {
        "id": "fgbio_CollectDuplexSeqMetrics_duplex_family_sizes",
        "title": "Fgbio: Frequency of duplex family sizes",
        "ylab": "Count",
        "xlab": "Duplex family size",
        "xDecimals": False,
        "tt_label": "<b>family size {point.x}</b>: {point.y}",
        "data_labels": [
            {"name": "Count", "ylab": "Count"},
            {"name": "Fraction", "ylab": "Fraction"},
        ],
    }

    # Build a list of linegraphs
    linegraph_data_simplex_family_size = [{}, {}]
    linegraph_data_duplex_family_size = [{}, {}]
    for s_name, s_data in family_sizes_data.items():
        linegraph_data_simplex_family_size[0][s_name] = {}
        linegraph_data_simplex_family_size[1][s_name] = {}

        linegraph_data_duplex_family_size[0][s_name] = {}
        linegraph_data_duplex_family_size[1][s_name] = {}

        for family_size, family_size_data in s_data.items():
            linegraph_data_simplex_family_size[0][s_name][family_size] = family_size_data['ss_count']
            linegraph_data_simplex_family_size[1][s_name][family_size] = family_size_data['ss_fraction']

            linegraph_data_duplex_family_size[0][s_name][family_size] = family_size_data['ds_count']
            linegraph_data_duplex_family_size[1][s_name][family_size] = family_size_data['ds_fraction']

    # build linegraphs for duplex yield metrics

    linegraph_data_duplex_yield_metrics = [{}, {}, {}, {}, {}, {}, {}]
    for s_name, s_data in duplex_yield_metrics_data.items():
        for i in range(len(linegraph_data_duplex_yield_metrics)):
            linegraph_data_duplex_yield_metrics[i][s_name] = {}

        for fraction, fraction_data in s_data.items():
            linegraph_data_duplex_yield_metrics[6][s_name][fraction] = fraction_data['read_pairs']
            linegraph_data_duplex_yield_metrics[5][s_name][fraction] = fraction_data['cs_families']
            linegraph_data_duplex_yield_metrics[4][s_name][fraction] = fraction_data['ss_families']
            linegraph_data_duplex_yield_metrics[3][s_name][fraction] = fraction_data['ds_families']
            linegraph_data_duplex_yield_metrics[2][s_name][fraction] = fraction_data['ds_duplexes']
            linegraph_data_duplex_yield_metrics[1][s_name][fraction] = \
                fraction_data['ds_fraction_duplexes_ideal']
            linegraph_data_duplex_yield_metrics[0][s_name][fraction] = fraction_data['ds_fraction_duplexes']

    pconfig_duplex_yield_metrics = {
        "id": "fgbio_CollectDuplexSeqMetrics_duplex_yield_metrics",
        "title": "Fgbio: Duplex yield metrics",
        "xlab": "Downsampling percentage",
        "xDecimals": True,
        "tt_label": "<b>percentage downsampled {point.x}</b>: {point.y}",
        "data_labels": [
            {"name": "DS fraction duplexes", "ylab": "DS fraction duplexes"},
            {"name": "DS fraction duplexes (ideal)", "ylab": "DS fraction duplexes (ideal)"},
            {"name": "DS duplex count", "ylab": "DS duplex count"},
            {"name": "DS family count", "ylab": "DS family count"},
            {"name": "SS family count", "ylab": "SS family count"},
            {"name": "CS family count", "ylab": "CS family count"},
            {"name": "Read pairs", "ylab": "Read pair count"},
        ],
    }


    # add a section for the plot
    self.add_section(
        name="Duplex family sizes",
        anchor="fgbio-freqency-duplex-family-sizes",
        description="Plot showing either the count or frequency of each duplex family size for each sample.",
        helptext="""
        Metrics produced by CollectDuplexSeqMetrics to describe the distribution of double-stranded (duplex) tag families in terms of the number of reads observed on each strand.We refer to the two strands as ab and ba because we identify the two strands by observing the same pair of UMIs (A and B) in opposite order (A->B vs B->A). Which strand is ab and which is ba is largely arbitrary, so to make interpretation of the metrics simpler we use a definition here that for a given tag family ab is the sub-family with more reads and ba is the tag family with fewer reads.
        """,
        plot=linegraph.plot(linegraph_data_duplex_family_size, pconfig_duplex_family_size),
    )

    self.add_section(
        name="Simplex family sizes",
        anchor="fgbio-freqency-simplex-family-sizes",
        description="Plot showing either the count or frequency of each simplex family size for each sample.",
        helptext="""
        Metrics produced by CollectDuplexSeqMetrics to describe the distribution of double-stranded (duplex) tag families in terms of the number of reads observed on each strand.We refer to the two strands as ab and ba because we identify the two strands by observing the same pair of UMIs (A and B) in opposite order (A->B vs B->A). Which strand is ab and which is ba is largely arbitrary, so to make interpretation of the metrics simpler we use a definition here that for a given tag family ab is the sub-family with more reads and ba is the tag family with fewer reads.
        """,
        plot=linegraph.plot(linegraph_data_simplex_family_size, pconfig_simplex_family_size),
    )

    self.add_section(
        name="Duplex yield metrics",
        anchor="fgbio-freqency-duplex-yield-metrics",
        description="Plots that show metrics produced by CollectDuplexSeqMetrics that are sampled at various levels of coverage, via random downsampling, during the construction of duplex metrics.",
        helptext="""
        Metrics produced by CollectDuplexSeqMetrics that are sampled at various levels of coverage, via random downsampling, during the construction of duplex metrics. The downsampling is done in such a way that the fractions are approximate, and not exact, therefore the fraction field should only be interpreted as a guide and the read_pairs field used to quantify how much data was used.See FamilySizeMetric for detailed definitions of CS, SS and DS as used below.
        """,
        plot=linegraph.plot(linegraph_data_duplex_yield_metrics, pconfig_duplex_yield_metrics),
    )

    return len(family_sizes_data)


def parse_duplex_yield_metrics(self):

    parse_data = dict()

    for f in self.find_log_files("fgbio/collectduplexseqmetrics_yield_metrics", filehandles=True):
        fh = f["f"]
        header = fh.readline().rstrip("\r\n").split("\t")

        if not header or header[0] != "fraction":
            continue

        # slurp in the data for this sample
        s_name = f["s_name"]
        s_data = dict()

        for line in fh:
            fields = line.rstrip("\r\n").split("\t")
            assert len(fields) == len(header), "Missing fields in line: `{}`".format(line)
            fields[0] = float(fields[0])
            fields[1:6] = [int(field) for field in fields[1:6]]
            fields[6:8] = [float(field) for field in fields[6:8]]

            row_data = dict(zip(header, fields))
            family_size = row_data["fraction"]
            s_data[family_size] = row_data

        if s_data:
            parse_data[s_name] = s_data

    # ignore samples
    parse_data = self.ignore_samples(parse_data)

    # if no data, then do nothing
    if not parse_data:
        return {}

    # Write parsed data to a file
    self.write_data_file(parse_data, "multiqc_fgbio_CollectDuplexSeqMetrics_duplex_yield_metrics")

    return parse_data


def parse_family_sizes(self):
    parsed_data = dict()

    for f in self.find_log_files("fgbio/collectduplexseqmetrics_family_sizes", filehandles=True):
        fh = f["f"]
        header = fh.readline().rstrip("\r\n").split("\t")

        if not header or header[0] != "family_size":
            continue

        # slurp in the data for this sample
        s_name = f["s_name"]
        s_data = dict()

        for line in fh:
            fields = line.rstrip("\r\n").split("\t")
            assert len(fields) == len(header), "Missing fields in line: `{}`".format(line)
            fields[0:2] = [int(field) for field in fields[0:2]]
            fields[2:4] = [float(field) for field in fields[2:4]]
            fields[4] = int(fields[4])
            fields[5:7] = [float(field) for field in fields[5:7]]
            fields[7] = int(fields[7])
            fields[8:10] = [float(field) for field in fields[8:10]]

            row_data = dict(zip(header, fields))
            family_size = row_data["family_size"]
            s_data[family_size] = row_data

        if s_data:
            parsed_data[s_name] = s_data

    # ignore samples
    parsed_data = self.ignore_samples(parsed_data)

    # if no data, then do nothing
    if not parsed_data:
        return {}

    # Write parsed data to a file
    self.write_data_file(parsed_data, "multiqc_fgbio_CollectDuplexSeqMetrics_family_sizes")

    return parsed_data
