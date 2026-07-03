"""Species metadata and sidebar display helpers."""

import streamlit as st

SPECIES_INFO = {
    "Megaptera novaeangliae": {
        "common_name": "Humpback whale",
        "length": "12–16 m",
        "weight": "25–40 tonnes",
        "status": "Least Concern",
        "description": (
            "Known for long migrations, complex songs, "
            "and acrobatic surface behaviour."
        ),
    }
}


def show_species_info(selected_species: list[str]) -> None:
    """Show species information when one known species is selected."""
    if len(selected_species) != 1:
        return

    species_name = selected_species[0]
    if species_name not in SPECIES_INFO:
        return

    info = SPECIES_INFO[species_name]

    st.sidebar.markdown("### Species info")
    st.sidebar.write(f"**Common name:** {info['common_name']}")
    st.sidebar.write(f"**Length:** {info['length']}")
    st.sidebar.write(f"**Weight:** {info['weight']}")
    st.sidebar.write(f"**IUCN status:** {info['status']}")
    st.sidebar.write(info["description"])
