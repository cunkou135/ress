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
  "scenario": "deffuant",
  "public_simulator": {
    "scenario": "deffuant",
    "description": "Agents on an initially rewired degree-eight network assimilate when opinions are close, may move apart under sufficiently distant encounters, and adapt rejected or backfire ties through fixed-probability rewiring.",
    "agent_rules": [
      "Each agent samples one neighbour from the current undirected network per step.",
      "Opinion distance within confidence_bound produces assimilation proportional to assimilation_strength.",
      "Distance at least backfire_threshold produces a weak repulsive update when the mechanism is enabled.",
      "Other encounters are rejected and opinions remain bounded to [-1, 1].",
      "Rejected or backfire encounters may replace the sampled tie at a fixed adaptive_rewiring_probability; replacement candidates exclude self-loops and duplicate edges, preserve at least one tie per agent, and use a disclosed weak homophilic preference.",
      "The time-varying fixed-edge-count edge list records the network used at the start of each step; successful rewiring affects the next step.",
      "Disabling backfire sets repulsive update strength to zero while preserving rejection-triggered adaptive rewiring."
    ],
    "controllable_parameters": [
      {
        "name": "confidence_bound",
        "meaning": "largest opinion distance that permits assimilation",
        "baseline": 0.35,
        "minus": 0.22,
        "plus": 0.5
      },
      {
        "name": "assimilation_strength",
        "meaning": "fraction of partner difference applied during assimilation",
        "baseline": 0.25,
        "minus": 0.12,
        "plus": 0.4
      },
      {
        "name": "backfire_threshold",
        "meaning": "opinion distance at which repulsive updating becomes possible",
        "baseline": 0.65,
        "minus": 0.5,
        "plus": 0.82
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
        "field_name": "state_opinion",
        "dtype": "float32",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "agent opinions bounded to [-1, 1] before each step update",
        "entity_level": "agent",
        "primitive_family": "opinion_state",
        "statistic_role": "individual_state"
      },
      {
        "field_name": "network_edges",
        "dtype": "int32",
        "shape": [
          "time",
          "edge",
          "endpoint"
        ],
        "semantic_meaning": "undirected interaction-network endpoint pairs used for partner sampling at the start of each step",
        "entity_level": "edge",
        "primitive_family": "network_topology",
        "statistic_role": "system_structure"
      },
      {
        "field_name": "partner_id",
        "dtype": "int32",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "network neighbour sampled by each agent at each step",
        "entity_level": "interaction",
        "primitive_family": "interaction_partner",
        "statistic_role": "interaction_record"
      },
      {
        "field_name": "interaction_distance",
        "dtype": "float32",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "absolute opinion distance in each sampled interaction",
        "entity_level": "interaction",
        "primitive_family": "encounter_distance",
        "statistic_role": "interaction_measure"
      },
      {
        "field_name": "interaction_accepted",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether sampled opinion distance permits assimilation",
        "entity_level": "interaction",
        "primitive_family": "assimilation_event",
        "statistic_role": "interaction_event"
      },
      {
        "field_name": "interaction_backfire",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether sampled opinion distance triggers repulsive updating",
        "entity_level": "interaction",
        "primitive_family": "repulsion_event",
        "statistic_role": "interaction_event"
      },
      {
        "field_name": "interaction_rejected",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether an interaction produces neither assimilation nor repulsion",
        "entity_level": "interaction",
        "primitive_family": "rejection_event",
        "statistic_role": "interaction_event"
      },
      {
        "field_name": "edge_rewired",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether the sampled rejected or backfire tie was successfully replaced for this focal agent",
        "entity_level": "interaction",
        "primitive_family": "rewiring_event",
        "statistic_role": "interaction_event"
      },
      {
        "field_name": "agent_shift",
        "dtype": "float32",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "signed opinion update applied to each agent",
        "entity_level": "agent",
        "primitive_family": "opinion_update",
        "statistic_role": "event_measure"
      },
      {
        "field_name": "sign_flip",
        "dtype": "bool",
        "shape": [
          "time",
          "agent"
        ],
        "semantic_meaning": "whether an update crosses opinion zero",
        "entity_level": "agent",
        "primitive_family": "sign_crossing_event",
        "statistic_role": "elementary_event"
      },
      {
        "field_name": "extreme_agent_count",
        "dtype": "int32",
        "shape": [
          "time"
        ],
        "semantic_meaning": "number of agents with absolute opinion at least 0.75",
        "entity_level": "system log aggregate",
        "primitive_family": "extreme_opinion_state",
        "statistic_role": "aggregate_count"
      }
    ],
    "public_environment_structure": {
      "initial_network_model": "Watts-Strogatz undirected fixed-edge-count network",
      "initial_network_rewire_probability": 0.08,
      "adaptive_rewiring_probability": 0.15,
      "rewiring_homophily_probability": 0.65,
      "adaptive_rule": "rejected or backfire encounters can replace the sampled tie; no self-loop, duplicate edge, or isolated agent is permitted and edge count is preserved"
    }
  },
  "indicator_set_sha256": "2bdcf2ab4711e8df29c32538341445f9ed4ca6cad90e57cb0d4f48dd6b49aa15",
  "frozen_indicators": [
    {
      "id": "micro_opinion_p25",
      "semantic_name": "25th percentile agent opinion",
      "scientific_definition": "Time series of the 25th percentile of pre-step agent opinions at each simulation step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "state_opinion"
      ],
      "computation": {
        "op": "quantile",
        "input": {
          "op": "field",
          "name": "state_opinion"
        },
        "axis": "agent",
        "q": 0.25
      },
      "parameter_associations": []
    },
    {
      "id": "micro_opinion_std",
      "semantic_name": "Agent opinion standard deviation",
      "scientific_definition": "Time series of the across-agent standard deviation of pre-step opinion values.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "state_opinion"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "field",
          "name": "state_opinion"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_median_opinion",
      "semantic_name": "Median agent opinion",
      "scientific_definition": "Time series of the across-agent median of pre-step opinion values.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "state_opinion"
      ],
      "computation": {
        "op": "quantile",
        "input": {
          "op": "field",
          "name": "state_opinion"
        },
        "axis": "agent",
        "q": 0.5
      },
      "parameter_associations": []
    },
    {
      "id": "micro_mean_interaction_distance",
      "semantic_name": "Mean sampled interaction opinion distance",
      "scientific_definition": "Time series of the across-agent mean absolute opinion distance in sampled interactions at each step.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "interaction_distance"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "field",
          "name": "interaction_distance"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_interaction_distance_std",
      "semantic_name": "Sampled interaction distance standard deviation",
      "scientific_definition": "Time series of the across-agent standard deviation of sampled interaction opinion distances.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "interaction_distance"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "field",
          "name": "interaction_distance"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_accepted_fraction",
      "semantic_name": "Assimilation encounter fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions that satisfy the closeness condition for assimilation.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "interaction_accepted"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "interaction_accepted"
        },
        "axis": "agent"
      },
      "parameter_associations": [
        {
          "parameter": "confidence_bound",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "A larger confidence bound permits assimilation at greater opinion distance, so the per-step fraction of accepted encounters should rise."
        }
      ]
    },
    {
      "id": "micro_backfire_fraction",
      "semantic_name": "Backfire encounter fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions that trigger repulsive updating at each step.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "interaction_backfire"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "interaction_backfire"
        },
        "axis": "agent"
      },
      "parameter_associations": [
        {
          "parameter": "backfire_threshold",
          "relationship": "direct",
          "expected_indicator_direction": "decrease",
          "rationale": "Raising the backfire threshold makes it harder for sampled opinion distances to qualify as sufficiently distant, reducing the expected backfire fraction."
        }
      ]
    },
    {
      "id": "micro_rejected_fraction",
      "semantic_name": "Rejected encounter fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions that produce neither assimilation nor repulsion.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "interaction_rejected"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "interaction_rejected"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_rewiring_fraction",
      "semantic_name": "Tie rewiring fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions in which the focal agent successfully replaced the sampled tie.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "edge_rewired"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "edge_rewired"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_mean_abs_agent_shift",
      "semantic_name": "Mean absolute opinion update",
      "scientific_definition": "Time series of the across-agent mean absolute signed opinion update applied at each step.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "agent_shift"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "abs",
          "input": {
            "op": "field",
            "name": "agent_shift"
          }
        },
        "axis": "agent"
      },
      "parameter_associations": [
        {
          "parameter": "assimilation_strength",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher assimilation strength increases the magnitude of opinion shifts in accepted encounters, thereby increasing the mean absolute update."
        }
      ]
    },
    {
      "id": "micro_agent_shift_std",
      "semantic_name": "Opinion update standard deviation",
      "scientific_definition": "Time series of the across-agent standard deviation of signed opinion updates.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "agent_shift"
      ],
      "computation": {
        "op": "std",
        "input": {
          "op": "field",
          "name": "agent_shift"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_sign_flip_fraction",
      "semantic_name": "Opinion sign-flip fraction",
      "scientific_definition": "Time series of the fraction of agents whose opinion update crosses zero at each step.",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "source_fields": [
        "sign_flip"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "field",
          "name": "sign_flip"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_extreme_agent_fraction",
      "semantic_name": "Extreme opinion fraction",
      "scientific_definition": "Time series of the fraction of agents with absolute pre-step opinion at least 0.75.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "state_opinion"
      ],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "greater_equal",
          "left": {
            "op": "abs",
            "input": {
              "op": "field",
              "name": "state_opinion"
            }
          },
          "right": {
            "op": "constant",
            "value": 0.75
          }
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_mean_abs_opinion",
      "semantic_name": "Mean absolute agent opinion",
      "scientific_definition": "Time series of the across-agent mean of absolute pre-step opinion values.",
      "scale": "micro",
      "entity_scope": "individual",
      "source_fields": [
        "state_opinion"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "abs",
          "input": {
            "op": "field",
            "name": "state_opinion"
          }
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_accepted_count",
      "semantic_name": "Accepted interaction count",
      "scientific_definition": "Time series of the total number of accepted sampled interactions across agents at each step.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "interaction_accepted"
      ],
      "computation": {
        "op": "count",
        "input": {
          "op": "field",
          "name": "interaction_accepted"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "micro_edge_rewired_count",
      "semantic_name": "Rewired tie count",
      "scientific_definition": "Time series of the total number of successful focal-agent tie replacements at each step.",
      "scale": "micro",
      "entity_scope": "interaction",
      "source_fields": [
        "edge_rewired"
      ],
      "computation": {
        "op": "count",
        "input": {
          "op": "field",
          "name": "edge_rewired"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_opinion_std",
      "semantic_name": "Mean neighborhood opinion standard deviation",
      "scientific_definition": "Time series of the across-agent mean of the standard deviation of opinions within each agent's current network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "state_opinion",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "field",
            "name": "state_opinion"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "std"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_opinion_variance",
      "semantic_name": "Mean neighborhood opinion variance",
      "scientific_definition": "Time series of the across-agent mean of the variance of opinions within each agent's current network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "state_opinion",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "field",
            "name": "state_opinion"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "variance"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_abs_opinion_std",
      "semantic_name": "Mean neighborhood absolute opinion standard deviation",
      "scientific_definition": "Time series of the across-agent mean of the standard deviation of absolute opinions within each agent's current network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "state_opinion",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "abs",
            "input": {
              "op": "field",
              "name": "state_opinion"
            }
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "std"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_abs_opinion_variance",
      "semantic_name": "Mean neighborhood absolute opinion variance",
      "scientific_definition": "Time series of the across-agent mean of the variance of absolute opinions within each agent's current network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "state_opinion",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "abs",
            "input": {
              "op": "field",
              "name": "state_opinion"
            }
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "variance"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_interaction_distance_std",
      "semantic_name": "Mean neighborhood interaction distance standard deviation",
      "scientific_definition": "Time series of the across-agent mean of the standard deviation of sampled interaction distances within each agent's network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "interaction_distance",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "field",
            "name": "interaction_distance"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "std"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_interaction_distance_variance",
      "semantic_name": "Mean neighborhood interaction distance variance",
      "scientific_definition": "Time series of the across-agent mean of the variance of sampled interaction distances within each agent's network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "interaction_distance",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "field",
            "name": "interaction_distance"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "variance"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_agent_shift_std",
      "semantic_name": "Mean neighborhood opinion shift standard deviation",
      "scientific_definition": "Time series of the across-agent mean of the standard deviation of signed opinion shifts within each agent's network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "agent_shift",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "field",
            "name": "agent_shift"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "std"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "meso_neighborhood_agent_shift_variance",
      "semantic_name": "Mean neighborhood opinion shift variance",
      "scientific_definition": "Time series of the across-agent mean of the variance of signed opinion shifts within each agent's network neighborhood.",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "source_fields": [
        "agent_shift",
        "network_edges"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "field",
            "name": "agent_shift"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "variance"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "macro_opinion_global_mean",
      "semantic_name": "Whole-system mean opinion",
      "scientific_definition": "Time series of the whole-system arithmetic mean of pre-step agent opinions.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "state_opinion"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "field",
          "name": "state_opinion"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "macro_opinion_global_variance",
      "semantic_name": "Whole-system opinion variance",
      "scientific_definition": "Time series of the whole-system variance of pre-step agent opinions.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "state_opinion"
      ],
      "computation": {
        "op": "variance",
        "input": {
          "op": "field",
          "name": "state_opinion"
        },
        "axis": "agent"
      },
      "parameter_associations": []
    },
    {
      "id": "macro_network_largest_component_fraction",
      "semantic_name": "Largest network component fraction",
      "scientific_definition": "Time series of the fraction of agents in the largest connected component of the current interaction network.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "network_edges",
        "agent_count"
      ],
      "computation": {
        "op": "network_largest_component_fraction",
        "edges": {
          "op": "field",
          "name": "network_edges"
        },
        "node_count": {
          "op": "field",
          "name": "agent_count"
        }
      },
      "parameter_associations": []
    },
    {
      "id": "macro_network_assortativity",
      "semantic_name": "Network opinion assortativity",
      "scientific_definition": "Time series of degree-weighted opinion assortativity across the current interaction network.",
      "scale": "macro",
      "entity_scope": "whole_system",
      "source_fields": [
        "state_opinion",
        "network_edges"
      ],
      "computation": {
        "op": "network_assortativity",
        "values": {
          "op": "field",
          "name": "state_opinion"
        },
        "edges": {
          "op": "field",
          "name": "network_edges"
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
