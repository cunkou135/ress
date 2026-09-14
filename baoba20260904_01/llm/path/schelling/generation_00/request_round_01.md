# System

You are constructing an auditable, executable multiscale representation of an emergent phenomenon in an agent-based simulator.

Use only the supplied scenario rules, controllable parameter descriptions, raw-log field schema, generic computation grammar, capacity controls, and structural constraints. Obey the phase-specific schema: indicator generation constructs observables only; path generation may only reference the frozen observable identifiers supplied in its input.

Treat scale as a scientific entity contract, not as a time-window label. Micro denotes individual, interaction, elementary-event, or local primitive processes even when their prevalence is aggregated into a time series. Meso denotes real subset, neighborhood, district, community, cluster, or local-domain organization and must use a supplied grouping or network/spatial structural operation. Macro denotes a whole-system collective state. A rolling window, difference, normalization, or constant rescaling alone never changes scientific scale.

The supplied indicator and candidate-path budgets are capacity controls for this experiment. They are not universal theoretical counts. In indicator generation, construct indicators from the public primitives and generic DSL while satisfying the typed entity_scope and scale rules. In path generation, never create, delete, rename, or modify an indicator.

The computation of every indicator must be a declarative JSON AST from the supplied grammar. Never output Python, source code, or an expression string. Complete candidate paths are semantic hypotheses only; adjacent edges are derived deterministically by the program. Do not claim statistical, causal, or intervention support. Prospective predictions must bind to candidate_path_id before any simulation statistics are observed and include an explicit falsification condition.

Return exactly one JSON object matching the supplied schema.
PHASE B ONLY: construct complete testable mechanism hypotheses from frozen observables. No new observable is permitted.

# User

Input contract:
{
  "phase": "path_hypothesis_generation",
  "scenario": "schelling",
  "public_simulator": {
    "scenario": "schelling",
    "description": "Agents of two groups occupy a periodic grid partitioned into fixed public spatial districts and may relocate when local same-group similarity is below tolerance.",
    "agent_rules": [
      "Each occupied cell contains one fixed-group agent and the grid is periodic.",
      "The periodic grid is partitioned into fixed public spatial districts; district membership follows an agent's current cell and is not a precomputed segregation outcome.",
      "An agent is unsatisfied when its occupied-neighbour same-group fraction is below tolerance.",
      "An unsatisfied agent attempts movement with move_probability.",
      "A moving agent samples vacancies and, with destination_preference, chooses the sampled vacancy with the highest local similarity.",
      "Disabling homophilic relocation makes destination choice non-preferential while preserving other rules."
    ],
    "controllable_parameters": [
      {
        "name": "tolerance",
        "meaning": "minimum local same-group fraction required for satisfaction",
        "baseline": 0.55,
        "minus": 0.4,
        "plus": 0.7
      },
      {
        "name": "move_probability",
        "meaning": "probability that an unsatisfied agent attempts relocation in one step",
        "baseline": 0.1,
        "minus": 0.05,
        "plus": 0.2
      },
      {
        "name": "destination_preference",
        "meaning": "probability of selecting the most similar sampled vacancy",
        "baseline": 0.8,
        "minus": 0.3,
        "plus": 1.0
      }
    ],
    "raw_field_schema": [
      {
        "field_name": "num_steps",
        "dtype": "int32",
        "shape": [
          1
        ],
        "semantic_meaning": "number of recorded simulation steps",
        "entity_level": "run",
        "primitive_family": "simulation_length",
        "statistic_role": "normalizer"
      },
      {
        "field_name": "agent_count",
        "dtype": "int32",
        "shape": [
          1
        ],
        "semantic_meaning": "number of agents in the simulation",
        "entity_level": "run",
        "primitive_family": "population_size",
        "statistic_role": "normalizer"
      },
      {
        "field_name": "state_grid",
        "dtype": "int8",
        "shape": [
          "time",
          "grid_y",
          "grid_x"
        ],
        "semantic_meaning": "periodic occupancy grid with -1 for vacancy and 0 or 1 for group",
        "entity_level": "cell",
        "primitive_family": "spatial_configuration",
        "statistic_role": "system_state"
      },
      {
        "field_name": "agent_id",
        "dtype": "int32",
        "shape": [
          "agent"
        ],
        "semantic_meaning": "stable public identifier of each agent",
        "entity_level": "agent",
        "primitive_family": "agent_identity",
        "statistic_role": "identifier"
      },
      {
        "field_name": "agent_group",
        "dtype": "int8",
        "shape": [
          "agent"
        ],
        "semantic_meaning": "fixed group label of each agent",
        "entity_level": "agent",
        "primitive_family": "social_group",
        "statistic_role": "categorical_state"
      },
      {
        "field_name": "agent_position",
        "dtype": "int32",
        "shape": [
          "time",
          "agent",
          "coordinate"
        ],
        "semantic_meaning": "row and column occupied by every agent",
        "entity_level": "agent",
        "primitive_family": "spatial_position",
        "statistic_role": "individual_state"
      },
      {
        "field_name": "district_id",
        "dtype": "int16",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "fixed spatial district containing each agent at the start of the recorded step",
        "entity_level": "district membership",
        "primitive_family": "district_membership",
        "statistic_role": "membership"
      },
      {
        "field_name": "local_similarity",
        "dtype": "float32",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "same-group fraction among occupied Moore neighbours",
        "entity_level": "agent",
        "primitive_family": "local_group_exposure",
        "statistic_role": "individual_measure"
      },
      {
        "field_name": "neighbour_count",
        "dtype": "int16",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "occupied Moore-neighbour count",
        "entity_level": "agent",
        "primitive_family": "local_occupancy",
        "statistic_role": "individual_measure"
      },
      {
        "field_name": "unhappy",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether local similarity is below tolerance",
        "entity_level": "agent",
        "primitive_family": "dissatisfaction_event",
        "statistic_role": "elementary_event"
      },
      {
        "field_name": "unhappy_count",
        "dtype": "int32",
        "shape": [
          "time"
        ],
        "semantic_meaning": "number of unsatisfied agents in each step",
        "entity_level": "system log aggregate",
        "primitive_family": "dissatisfaction_event",
        "statistic_role": "aggregate_count"
      },
      {
        "field_name": "moved",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether the agent relocated during the step",
        "entity_level": "agent",
        "primitive_family": "relocation_event",
        "statistic_role": "elementary_event"
      },
      {
        "field_name": "move_distance",
        "dtype": "float32",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "periodic Manhattan distance of relocation, zero without a move",
        "entity_level": "agent",
        "primitive_family": "relocation_distance",
        "statistic_role": "event_measure"
      },
      {
        "field_name": "destination_similarity",
        "dtype": "float32",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "same-group neighbour fraction at the selected destination, zero without a move",
        "entity_level": "agent",
        "primitive_family": "destination_exposure",
        "statistic_role": "event_measure"
      },
      {
        "field_name": "boundary_agent",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether an agent has at least one occupied different-group neighbour",
        "entity_level": "agent",
        "primitive_family": "boundary_exposure",
        "statistic_role": "binary_state"
      }
    ],
    "public_environment_structure": {
      "periodic_grid": true,
      "district_rows": 3,
      "district_columns": 3,
      "district_semantics": "fixed spatial domains defined before simulation; district_id is a primitive membership label, not an inferred outcome"
    }
  },
  "indicator_set_sha256": "e8bf22736392ff1b49e8a923a374cfeaa351e9a1ca58477d538f69115470cc78",
  "frozen_indicators": [
    {
      "id": "mean_local_similarity",
      "semantic_name": "Mean local same-group similarity",
      "scientific_definition": "Mean occupied-neighbour same-group fraction across agents at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "local_similarity"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "field",
          "name": "local_similarity"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "std_local_similarity",
      "semantic_name": "Standard deviation of local same-group similarity",
      "scientific_definition": "Cross-agent dispersion of occupied-neighbour same-group fraction at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "local_similarity"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "field",
          "name": "local_similarity"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "mean_neighbour_count",
      "semantic_name": "Mean local neighbour count",
      "scientific_definition": "Mean occupied Moore-neighbour count across agents at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "neighbour_count"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "field",
          "name": "neighbour_count"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "unhappy_fraction",
      "semantic_name": "Fraction of unsatisfied agents",
      "scientific_definition": "Proportion of agents whose local same-group fraction is below tolerance at each step, computed as the boolean dissatisfaction event fraction over agents.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "unhappy"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "unhappy"
        },
        "axis": "agent"
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher tolerance raises the minimum required same-group fraction, so more agents are classified as unsatisfied."
        }
      ]
    },
    {
      "id": "unhappy_local_similarity_mean",
      "semantic_name": "Mean local similarity among unsatisfied agents",
      "scientific_definition": "Mean local same-group fraction among agents classified as unsatisfied at each step, excluding satisfied agents by boolean masking.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "unhappy",
        "local_similarity"
      ],
      "computation": {
        "op": "safe_ratio",
        "left": {
          "op": "sum",
          "input": {
            "op": "where",
            "condition": {
              "op": "field",
              "name": "unhappy"
            },
            "input": {
              "op": "field",
              "name": "local_similarity"
            }
          },
          "axis": "agent"
        },
        "right": {
          "op": "count",
          "input": {
            "op": "field",
            "name": "unhappy"
          },
          "axis": "agent"
        }
      },
      "parameter_associations": []
    },
    {
      "id": "moved_fraction",
      "semantic_name": "Fraction of agents relocating",
      "scientific_definition": "Proportion of agents that relocated during each recorded step, computed as the boolean relocation event fraction over agents.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "moved"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "moved"
        },
        "axis": "agent"
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move_probability increases the chance an unsatisfied agent attempts relocation, raising the fraction that moves."
        }
      ]
    },
    {
      "id": "mean_move_distance",
      "semantic_name": "Mean relocation distance among movers",
      "scientific_definition": "Mean periodic Manhattan distance of relocation among agents that moved during each step, excluding non-movers.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "moved",
        "move_distance"
      ],
      "computation": {
        "op": "safe_ratio",
        "left": {
          "op": "sum",
          "input": {
            "op": "where",
            "condition": {
              "op": "field",
              "name": "moved"
            },
            "input": {
              "op": "field",
              "name": "move_distance"
            }
          },
          "axis": "agent"
        },
        "right": {
          "op": "count",
          "input": {
            "op": "field",
            "name": "moved"
          },
          "axis": "agent"
        }
      },
      "parameter_associations": []
    },
    {
      "id": "mean_destination_similarity_movers",
      "semantic_name": "Mean destination similarity among movers",
      "scientific_definition": "Mean same-group neighbour fraction at selected destinations among agents that relocated during each step, excluding non-movers.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "moved",
        "destination_similarity"
      ],
      "computation": {
        "op": "safe_ratio",
        "left": {
          "op": "sum",
          "input": {
            "op": "where",
            "condition": {
              "op": "field",
              "name": "moved"
            },
            "input": {
              "op": "field",
              "name": "destination_similarity"
            }
          },
          "axis": "agent"
        },
        "right": {
          "op": "count",
          "input": {
            "op": "field",
            "name": "moved"
          },
          "axis": "agent"
        }
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher destination_preference increases the probability of selecting the most similar sampled vacancy, raising average destination similarity among movers."
        }
      ]
    },
    {
      "id": "boundary_fraction",
      "semantic_name": "Fraction of boundary agents",
      "scientific_definition": "Proportion of agents with at least one occupied different-group neighbour at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "boundary_agent"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "boundary_agent"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "std_destination_similarity",
      "semantic_name": "Dispersion of destination similarity",
      "scientific_definition": "Cross-agent standard deviation of destination same-group neighbour fraction, including zero for non-movers, at each step.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "destination_similarity"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "field",
          "name": "destination_similarity"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "quantile_25_local_similarity",
      "semantic_name": "25th percentile local similarity",
      "scientific_definition": "Lower quartile of agents' local same-group fraction at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "local_similarity"
      ],
      "computation": {
        "op": "quantile",
        "input": {
          "op": "field",
          "name": "local_similarity"
        },
        "axis": "agent",
        "q": 0.25
      },
      "parameter_associations": []
    },
    {
      "id": "quantile_75_local_similarity",
      "semantic_name": "75th percentile local similarity",
      "scientific_definition": "Upper quartile of agents' local same-group fraction at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "local_similarity"
      ],
      "computation": {
        "op": "quantile",
        "input": {
          "op": "field",
          "name": "local_similarity"
        },
        "axis": "agent",
        "q": 0.75
      },
      "parameter_associations": []
    },
    {
      "id": "local_similarity_entropy",
      "semantic_name": "Entropy of local similarity distribution",
      "scientific_definition": "Shannon entropy of binned local same-group similarity across agents at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "local_similarity"
      ],
      "computation": {
        "op": "binned_entropy",
        "input": {
          "op": "field",
          "name": "local_similarity"
        },
        "axis": "agent",
        "bins": 10
      },
      "parameter_associations": []
    },
    {
      "id": "move_distance_std",
      "semantic_name": "Dispersion of relocation distance",
      "scientific_definition": "Cross-agent standard deviation of periodic Manhattan relocation distance, including zero for non-movers, at each step.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "move_distance"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "field",
          "name": "move_distance"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "std_neighbour_count",
      "semantic_name": "Dispersion of local neighbour count",
      "scientific_definition": "Cross-agent standard deviation of occupied Moore-neighbour count at each recorded step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "neighbour_count"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "field",
          "name": "neighbour_count"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "relocation_response_fraction",
      "semantic_name": "Relocation response fraction",
      "scientific_definition": "Ratio of moving agents to unsatisfied agents at each step, measuring the realized relocation response among dissatisfied agents.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "moved",
        "unhappy"
      ],
      "computation": {
        "op": "safe_ratio",
        "left": {
          "op": "count",
          "input": {
            "op": "field",
            "name": "moved"
          },
          "axis": "agent"
        },
        "right": {
          "op": "count",
          "input": {
            "op": "field",
            "name": "unhappy"
          },
          "axis": "agent"
        }
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move_probability increases the chance that an unsatisfied agent attempts relocation, raising the ratio of movers to unsatisfied agents."
        }
      ]
    },
    {
      "id": "meso_district_local_similarity_std",
      "semantic_name": "Between-district standard deviation of mean local similarity",
      "scientific_definition": "Cross-district dispersion of district-averaged local same-group similarity at each recorded step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "local_similarity",
        "district_id"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "local_similarity"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "mean"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_district_unhappy_fraction_std",
      "semantic_name": "Between-district standard deviation of unsatisfied fraction",
      "scientific_definition": "Cross-district dispersion of district-level unsatisfied-agent fraction at each recorded step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "unhappy",
        "district_id"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "unhappy"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "fraction"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_district_boundary_fraction_std",
      "semantic_name": "Between-district standard deviation of boundary-agent fraction",
      "scientific_definition": "Cross-district dispersion of the district-level proportion of agents with at least one different-group neighbour at each step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "boundary_agent",
        "district_id"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "boundary_agent"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "fraction"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_district_move_fraction_std",
      "semantic_name": "Between-district standard deviation of moving fraction",
      "scientific_definition": "Cross-district dispersion of the district-level proportion of agents that relocated during each recorded step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "moved",
        "district_id"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "moved"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "fraction"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_district_destination_similarity_std",
      "semantic_name": "Between-district standard deviation of destination similarity",
      "scientific_definition": "Cross-district dispersion of district-averaged destination same-group neighbour fraction at each recorded step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "destination_similarity",
        "district_id"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "destination_similarity"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "mean"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_district_neighbour_count_std",
      "semantic_name": "Between-district standard deviation of mean neighbour count",
      "scientific_definition": "Cross-district dispersion of district-averaged occupied Moore-neighbour count at each recorded step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "neighbour_count",
        "district_id"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "neighbour_count"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "mean"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_district_group_entropy_mean",
      "semantic_name": "Mean district group-composition entropy",
      "scientific_definition": "Average district-level entropy of agent group labels within each fixed public district at each recorded step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "agent_group",
        "district_id"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "agent_group"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "entropy"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_district_move_distance_std",
      "semantic_name": "Between-district standard deviation of mean move distance",
      "scientific_definition": "Cross-district dispersion of district-averaged periodic Manhattan relocation distance at each recorded step.",
      "scale": "meso",
      "entity_scope": "district",
      "source_fields": [
        "move_distance",
        "district_id"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "group_reduce",
          "values": {
            "op": "field",
            "name": "move_distance"
          },
          "groups": {
            "op": "field",
            "name": "district_id"
          },
          "axis": "agent",
          "reducer": "mean"
        },
        "axis": "group"
      },
      "parameter_associations": []
    },
    {
      "id": "macro_global_unhappy_fraction",
      "semantic_name": "Global unsatisfied fraction",
      "scientific_definition": "Whole-system proportion of unsatisfied agents computed from the system aggregate unsatisfied count at each recorded step.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "unhappy_count",
        "agent_count"
      ],
      "computation": {
        "op": "divide",
        "left": {
          "op": "field",
          "name": "unhappy_count"
        },
        "right": {
          "op": "field",
          "name": "agent_count"
        }
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher tolerance increases the global number of unsatisfied agents, raising the whole-system unsatisfied fraction."
        }
      ]
    },
    {
      "id": "macro_global_moved_fraction",
      "semantic_name": "Global relocation fraction",
      "scientific_definition": "Whole-system proportion of agents that relocated during each recorded step, computed as the ratio of relocation-event count to agent population.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "moved",
        "agent_count"
      ],
      "computation": {
        "op": "divide",
        "left": {
          "op": "count",
          "input": {
            "op": "field",
            "name": "moved"
          },
          "axis": "agent"
        },
        "right": {
          "op": "field",
          "name": "agent_count"
        }
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move_probability increases the global relocation frequency, raising the whole-system moving fraction."
        }
      ]
    },
    {
      "id": "macro_global_connected_components",
      "semantic_name": "Count of same-group spatial components",
      "scientific_definition": "Number of contiguous occupied-cell components with identical group label in the periodic grid at each recorded step, excluding vacancies.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "state_grid"
      ],
      "computation": {
        "op": "connected_component_count",
        "input": {
          "op": "field",
          "name": "state_grid"
        }
      },
      "parameter_associations": []
    },
    {
      "id": "macro_global_spatial_neighbor_similarity",
      "semantic_name": "Global spatial neighbour similarity",
      "scientific_definition": "Whole-grid average same-group similarity among occupied Moore neighbours at each recorded step.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "state_grid"
      ],
      "computation": {
        "op": "spatial_neighbor_similarity",
        "input": {
          "op": "field",
          "name": "state_grid"
        }
      },
      "parameter_associations": []
    }
  ],
  "candidate_path_bounds": {
    "minimum": 16,
    "maximum": 24
  },
  "constraints": [
    "Use only the supplied frozen indicator IDs; never create or modify an observable.",
    "Every hypothesis is a complete parameter to Micro to Meso to Macro mechanism path.",
    "Cover every controllable parameter with at least four paths.",
    "Cover every frozen Macro endpoint with at least two paths.",
    "Do not repeat an identical Micro-Meso-Macro triple.",
    "Only the primary accepted generation enters Stage 2 and Stage 3.",
    "Return six prospective predictions bound to candidate_path_id values.",
    "Do not use or request simulation outcomes."
  ]
}

Output JSON schema:
{
  "$defs": {
    "CandidatePath": {
      "additionalProperties": false,
      "properties": {
        "path_id": {
          "pattern": "^[a-z][a-z0-9_]{2,95}$",
          "title": "Path Id",
          "type": "string"
        },
        "parameter": {
          "title": "Parameter",
          "type": "string"
        },
        "intervention_direction": {
          "enum": [
            "minus",
            "plus"
          ],
          "title": "Intervention Direction",
          "type": "string"
        },
        "micro_indicator": {
          "title": "Micro Indicator",
          "type": "string"
        },
        "meso_indicator": {
          "title": "Meso Indicator",
          "type": "string"
        },
        "macro_indicator": {
          "title": "Macro Indicator",
          "type": "string"
        },
        "micro_to_meso_expected_direction": {
          "enum": [
            "increase",
            "decrease"
          ],
          "title": "Micro To Meso Expected Direction",
          "type": "string"
        },
        "meso_to_macro_expected_direction": {
          "enum": [
            "increase",
            "decrease"
          ],
          "title": "Meso To Macro Expected Direction",
          "type": "string"
        },
        "expected_micro_response": {
          "enum": [
            "increase",
            "decrease"
          ],
          "title": "Expected Micro Response",
          "type": "string"
        },
        "expected_meso_response": {
          "enum": [
            "increase",
            "decrease"
          ],
          "title": "Expected Meso Response",
          "type": "string"
        },
        "expected_macro_response": {
          "enum": [
            "increase",
            "decrease"
          ],
          "title": "Expected Macro Response",
          "type": "string"
        },
        "scientific_rationale": {
          "minLength": 12,
          "title": "Scientific Rationale",
          "type": "string"
        },
        "mechanistic_explanation": {
          "minLength": 12,
          "title": "Mechanistic Explanation",
          "type": "string"
        },
        "falsification_condition": {
          "minLength": 12,
          "title": "Falsification Condition",
          "type": "string"
        }
      },
      "required": [
        "path_id",
        "parameter",
        "intervention_direction",
        "micro_indicator",
        "meso_indicator",
        "macro_indicator",
        "micro_to_meso_expected_direction",
        "meso_to_macro_expected_direction",
        "expected_micro_response",
        "expected_meso_response",
        "expected_macro_response",
        "scientific_rationale",
        "mechanistic_explanation",
        "falsification_condition"
      ],
      "title": "CandidatePath",
      "type": "object"
    },
    "ProspectivePrediction": {
      "additionalProperties": false,
      "properties": {
        "prediction_id": {
          "pattern": "^[a-z][a-z0-9_]{2,95}$",
          "title": "Prediction Id",
          "type": "string"
        },
        "candidate_path_id": {
          "title": "Candidate Path Id",
          "type": "string"
        },
        "prospective_priority": {
          "default": 0,
          "minimum": 0,
          "title": "Prospective Priority",
          "type": "integer"
        },
        "scientific_rationale": {
          "minLength": 12,
          "title": "Scientific Rationale",
          "type": "string"
        },
        "falsification_condition": {
          "minLength": 12,
          "title": "Falsification Condition",
          "type": "string"
        }
      },
      "required": [
        "prediction_id",
        "candidate_path_id",
        "scientific_rationale",
        "falsification_condition"
      ],
      "title": "ProspectivePrediction",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "description": "Phase B response over one immutable indicator set.",
  "properties": {
    "scenario": {
      "title": "Scenario",
      "type": "string"
    },
    "indicator_set_sha256": {
      "pattern": "^[0-9a-f]{64}$",
      "title": "Indicator Set Sha256",
      "type": "string"
    },
    "candidate_paths": {
      "items": {
        "$ref": "#/$defs/CandidatePath"
      },
      "title": "Candidate Paths",
      "type": "array"
    },
    "prospective_predictions": {
      "items": {
        "$ref": "#/$defs/ProspectivePrediction"
      },
      "title": "Prospective Predictions",
      "type": "array"
    }
  },
  "required": [
    "scenario",
    "indicator_set_sha256",
    "candidate_paths",
    "prospective_predictions"
  ],
  "title": "PathGeneration",
  "type": "object"
}

The previous response failed only these schema/executability checks:
[
  "path tol_plus_sim_std_to_dist_sim_std_to_global_spatial_sim: Micro source lacks direct parameter association",
  "path tol_plus_q25_to_group_entropy_to_components: Micro source lacks direct parameter association",
  "path tol_minus_unhappy_to_unhappy_std_to_global_unhappy: trivial Micro-Macro lineage",
  "path tol_minus_boundary_to_boundary_std_to_spatial_sim: Micro source lacks direct parameter association",
  "path tol_minus_entropy_to_dest_std_to_components: Micro source lacks direct parameter association",
  "path move_plus_distance_to_dist_std_to_components: Micro source lacks direct parameter association",
  "path move_minus_distance_to_dist_std_to_global_unhappy: Micro source lacks direct parameter association",
  "path dest_plus_boundary_to_boundary_std_to_global_unhappy: Micro source lacks direct parameter association",
  "path dest_plus_dest_sim_std_to_dist_sim_std_to_components: Micro source lacks direct parameter association",
  "path dest_minus_distance_to_dist_std_to_spatial_sim: Micro source lacks direct parameter association"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "schelling",
  "indicator_set_sha256": "e8bf22736392ff1b49e8a923a374cfeaa351e9a1ca58477d538f69115470cc78",
  "candidate_paths": [
    {
      "path_id": "tol_plus_unhappy_to_move_std_to_global_moved",
      "parameter": "tolerance",
      "intervention_direction": "plus",
      "micro_indicator": "unhappy_fraction",
      "meso_indicator": "meso_district_move_fraction_std",
      "macro_indicator": "macro_global_moved_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher tolerance increases the fraction of agents classified as unsatisfied, which amplifies district-level differences in relocation activity and therefore raises the whole-system moved fraction.",
      "mechanistic_explanation": "More unsatisfied agents attempt relocation, increasing between-district dispersion of moving fractions, and this dispersed local activation raises the global relocation fraction.",
      "falsification_condition": "Observed meso_district_move_fraction_std or macro_global_moved_fraction does not increase under tolerance plus."
    },
    {
      "path_id": "tol_plus_sim_std_to_dist_sim_std_to_global_spatial_sim",
      "parameter": "tolerance",
      "intervention_direction": "plus",
      "micro_indicator": "std_local_similarity",
      "meso_indicator": "meso_district_local_similarity_std",
      "macro_indicator": "macro_global_spatial_neighbor_similarity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher tolerance intensifies segregation pressure, increasing cross-agent dispersion of local similarity; this dispersion propagates to district-level variation and raises global spatial neighbour similarity.",
      "mechanistic_explanation": "Stronger homophilic relocation produces more dissimilar local experiences across agents and districts while increasing whole-grid same-group neighbour similarity.",
      "falsification_condition": "Macro global spatial neighbour similarity does not increase when tolerance is increased."
    },
    {
      "path_id": "tol_plus_q25_to_group_entropy_to_components",
      "parameter": "tolerance",
      "intervention_direction": "plus",
      "micro_indicator": "quantile_25_local_similarity",
      "meso_indicator": "meso_district_group_entropy_mean",
      "macro_indicator": "macro_global_connected_components",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Higher tolerance depresses the lower tail of local similarity by driving agents out of mixed neighbourhoods; districts become more internally homogeneous, and the resulting consolidation reduces the number of same-group spatial components.",
      "mechanistic_explanation": "As the lower quartile of local similarity falls, district group entropy declines, and contiguous same-group areas merge into fewer components.",
      "falsification_condition": "Observed quantile_25_local_similarity or macro_global_connected_components does not decrease under tolerance plus."
    },
    {
      "path_id": "tol_minus_unhappy_to_unhappy_std_to_global_unhappy",
      "parameter": "tolerance",
      "intervention_direction": "minus",
      "micro_indicator": "unhappy_fraction",
      "meso_indicator": "meso_district_unhappy_fraction_std",
      "macro_indicator": "macro_global_unhappy_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Lower tolerance reduces the proportion of agents classified as unsatisfied, lowers between-district variation in dissatisfaction, and decreases the whole-system unsatisfied fraction.",
      "mechanistic_explanation": "Fewer agents fall below the lower tolerance threshold, so district-level dissatisfaction differences shrink and the global unsatisfied fraction falls.",
      "falsification_condition": "Macro global unsatisfied fraction does not decrease when tolerance is lowered."
    },
    {
      "path_id": "tol_minus_boundary_to_boundary_std_to_spatial_sim",
      "parameter": "tolerance",
      "intervention_direction": "minus",
      "micro_indicator": "boundary_fraction",
      "meso_indicator": "meso_district_boundary_fraction_std",
      "macro_indicator": "macro_global_spatial_neighbor_similarity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Lower tolerance relaxes homophilic pressure, allowing more mixed-group boundaries to persist; this raises district boundary-fraction dispersion while reducing global spatial neighbour similarity.",
      "mechanistic_explanation": "Increased boundary contacts propagate into more variable district boundary fractions, and the resulting mixing lowers whole-grid same-group neighbour similarity.",
      "falsification_condition": "Macro global spatial neighbour similarity does not decrease when tolerance is lowered."
    },
    {
      "path_id": "tol_minus_entropy_to_dest_std_to_components",
      "parameter": "tolerance",
      "intervention_direction": "minus",
      "micro_indicator": "local_similarity_entropy",
      "meso_indicator": "meso_district_destination_similarity_std",
      "macro_indicator": "macro_global_connected_components",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Lower tolerance permits greater diversity in local similarity, increasing entropy; this is accompanied by more variable destination similarity across districts and more fragmented spatial components.",
      "mechanistic_explanation": "Relaxed sorting preserves heterogeneous local experiences and district destination patterns, preventing large same-group clusters from consolidating and thus raising component count.",
      "falsification_condition": "Observed local_similarity_entropy or macro_global_connected_components does not increase under tolerance minus."
    },
    {
      "path_id": "move_plus_moved_to_move_std_to_global_moved",
      "parameter": "move_probability",
      "intervention_direction": "plus",
      "micro_indicator": "moved_fraction",
      "meso_indicator": "meso_district_move_fraction_std",
      "macro_indicator": "macro_global_moved_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher move probability directly increases the fraction of agents relocating, amplifies district-level differences in relocation, and raises the global moved fraction.",
      "mechanistic_explanation": "More unsatisfied agents attempt to move, so district move rates become more dispersed and global relocation activity increases.",
      "falsification_condition": "Macro global moved fraction does not increase when move_probability is increased."
    },
    {
      "path_id": "move_plus_moved_to_dest_std_to_spatial_sim",
      "parameter": "move_probability",
      "intervention_direction": "plus",
      "micro_indicator": "moved_fraction",
      "meso_indicator": "meso_district_destination_similarity_std",
      "macro_indicator": "macro_global_spatial_neighbor_similarity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher move probability increases relocation frequency, which creates more variable destination-similarity outcomes across districts and raises global spatial neighbour similarity through repeated homophilic sorting.",
      "mechanistic_explanation": "More moves allow more agents to enter high-similarity locations, increasing district-level destination-similarity dispersion and whole-grid same-group adjacency.",
      "falsification_condition": "Macro global spatial neighbour similarity does not increase under move_probability plus."
    },
    {
      "path_id": "move_plus_distance_to_dist_std_to_components",
      "parameter": "move_probability",
      "intervention_direction": "plus",
      "micro_indicator": "mean_move_distance",
      "meso_indicator": "meso_district_move_distance_std",
      "macro_indicator": "macro_global_connected_components",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher move probability increases average relocation distance, raises district-level dispersion of move distances, and fragments existing spatial clusters, increasing the count of same-group components.",
      "mechanistic_explanation": "Longer or more frequent relocations disrupt contiguous same-group regions and produce more disconnected spatial components.",
      "falsification_condition": "Macro global connected components does not increase when move_probability is increased."
    },
    {
      "path_id": "move_minus_response_to_move_std_to_global_moved",
      "parameter": "move_probability",
      "intervention_direction": "minus",
      "micro_indicator": "relocation_response_fraction",
      "meso_indicator": "meso_district_move_fraction_std",
      "macro_indicator": "macro_global_moved_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Lower move probability reduces the realized relocation response among unsatisfied agents, lowers district-level dispersion of moving rates, and decreases the global moved fraction.",
      "mechanistic_explanation": "Fewer unsatisfied agents act on dissatisfaction, so local activation differences shrink and whole-system relocation declines.",
      "falsification_condition": "Macro global moved fraction does not decrease when move_probability is lowered."
    },
    {
      "path_id": "move_minus_distance_to_dist_std_to_global_unhappy",
      "parameter": "move_probability",
      "intervention_direction": "minus",
      "micro_indicator": "mean_move_distance",
      "meso_indicator": "meso_district_move_distance_std",
      "macro_indicator": "macro_global_unhappy_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Lower move probability reduces average relocation distance and district-level distance dispersion, but because fewer unsatisfied agents relocate to better neighbourhoods, global dissatisfaction increases.",
      "mechanistic_explanation": "Reduced movement prevents relief of dissatisfaction, so while movement-related indicators fall, the global unsatisfied fraction rises.",
      "falsification_condition": "Macro global unhappy fraction does not increase when move_probability is lowered."
    },
    {
      "path_id": "dest_plus_dest_sim_to_dest_std_to_spatial_sim",
      "parameter": "destination_preference",
      "intervention_direction": "plus",
      "micro_indicator": "mean_destination_similarity_movers",
      "meso_indicator": "meso_district_destination_similarity_std",
      "macro_indicator": "macro_global_spatial_neighbor_similarity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher destination preference makes movers select more similar destinations, increasing average destination similarity and district-level destination-similarity dispersion, and raising global spatial neighbour similarity.",
      "mechanistic_explanation": "Selective relocation concentrates agents in high-similarity destinations, increasing cross-district variation in destination quality and whole-grid segregation.",
      "falsification_condition": "Macro global spatial neighbour similarity does not increase when destination_preference is increased."
    },
    {
      "path_id": "dest_plus_boundary_to_boundary_std_to_global_unhappy",
      "parameter": "destination_preference",
      "intervention_direction": "plus",
      "micro_indicator": "boundary_fraction",
      "meso_indicator": "meso_district_boundary_fraction_std",
      "macro_indicator": "macro_global_unhappy_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Higher destination preference moves agents away from mixed boundaries, reducing boundary-agent fraction and district boundary-fraction dispersion, and lowering global dissatisfaction as more agents reach satisfying neighbourhoods.",
      "mechanistic_explanation": "Stronger preference for similar destinations removes agents from boundary contact and reduces the share of unsatisfied agents system-wide.",
      "falsification_condition": "Macro global unhappy fraction does not decrease when destination_preference is increased."
    },
    {
      "path_id": "dest_plus_dest_sim_std_to_dist_sim_std_to_components",
      "parameter": "destination_preference",
      "intervention_direction": "plus",
      "micro_indicator": "std_destination_similarity",
      "meso_indicator": "meso_district_local_similarity_std",
      "macro_indicator": "macro_global_connected_components",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Higher destination preference creates greater dispersion in destination similarity across movers, amplifies district-level local similarity variation, and consolidates same-group areas into fewer connected components.",
      "mechanistic_explanation": "Strongly preferential moves increase inequality in destination outcomes, sharpen between-district sorting, and merge same-group clusters.",
      "falsification_condition": "Macro global connected components does not decrease when destination_preference is increased."
    },
    {
      "path_id": "dest_minus_distance_to_dist_std_to_spatial_sim",
      "parameter": "destination_preference",
      "intervention_direction": "minus",
      "micro_indicator": "mean_move_distance",
      "meso_indicator": "meso_district_move_distance_std",
      "macro_indicator": "macro_global_spatial_neighbor_similarity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Lower destination preference makes moves less selective, increasing average relocation distance and district-level distance dispersion, while more random mixing reduces global spatial neighbour similarity.",
      "mechanistic_explanation": "Random destination choices produce longer, more variable moves that disrupt same-group adjacency and lower whole-grid segregation.",
      "falsification_condition": "Macro global spatial neighbour similarity does not decrease when destination_preference is lowered."
    },
    {
      "path_id": "dest_minus_dest_sim_to_dest_std_to_global_unhappy",
      "parameter": "destination_preference",
      "intervention_direction": "minus",
      "micro_indicator": "mean_destination_similarity_movers",
      "meso_indicator": "meso_district_destination_similarity_std",
      "macro_indicator": "macro_global_unhappy_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Lower destination preference lowers the average similarity of chosen destinations and reduces district-level destination-similarity dispersion, but less effective sorting leaves more agents unsatisfied globally.",
      "mechanistic_explanation": "Weaker preference reduces destination quality and spatial differentiation while preventing dissatisfied agents from reaching satisfying neighbourhoods, raising global dissatisfaction.",
      "falsification_condition": "Macro global unhappy fraction does not increase when destination_preference is lowered."
    }
  ],
  "prospective_predictions": [
    {
      "prediction_id": "pred_tol_plus_moved_fraction",
      "candidate_path_id": "tol_plus_unhappy_to_move_std_to_global_moved",
      "scientific_rationale": "If the tolerance-to-moving chain holds, increasing tolerance should raise the global moved fraction through district-level relocation dispersion.",
      "falsification_condition": "Macro global moved fraction does not increase under tolerance plus."
    },
    {
      "prediction_id": "pred_tol_plus_spatial_similarity",
      "candidate_path_id": "tol_plus_sim_std_to_dist_sim_std_to_global_spatial_sim",
      "scientific_rationale": "Higher tolerance is expected to increase whole-grid same-group neighbour similarity via stronger sorting.",
      "falsification_condition": "Macro global spatial neighbour similarity does not increase under tolerance plus."
    },
    {
      "prediction_id": "pred_move_plus_moved_fraction",
      "candidate_path_id": "move_plus_moved_to_move_std_to_global_moved",
      "scientific_rationale": "Higher move probability should produce a higher global relocation fraction.",
      "falsification_condition": "Macro global moved fraction does not increase under move_probability plus."
    },
    {
      "prediction_id": "pred_move_minus_unhappy_fraction",
      "candidate_path_id": "move_minus_distance_to_dist_std_to_global_unhappy",
      "scientific_rationale": "Lower move probability is expected to raise global dissatisfaction because fewer unsatisfied agents relocate to better neighbourhoods.",
      "falsification_condition": "Macro global unhappy fraction does not increase under move_probability minus."
    },
    {
      "prediction_id": "pred_dest_plus_spatial_similarity",
      "candidate_path_id": "dest_plus_dest_sim_to_dest_std_to_spatial_sim",
      "scientific_rationale": "Higher destination preference should increase global spatial neighbour similarity through selective relocation.",
      "falsification_condition": "Macro global spatial neighbour similarity does not increase under destination_preference plus."
    },
    {
      "prediction_id": "pred_dest_plus_components",
      "candidate_path_id": "dest_plus_dest_sim_std_to_dist_sim_std_to_components",
      "scientific_rationale": "Higher destination preference is expected to consolidate same-group clusters, reducing the count of global connected components.",
      "falsification_condition": "Macro global connected components does not decrease under destination_preference plus."
    }
  ]
}
