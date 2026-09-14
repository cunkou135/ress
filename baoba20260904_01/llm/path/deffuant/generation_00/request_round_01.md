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

The previous response failed only these schema/executability checks:
[
  "path cb_plus_reject_assort: Micro source lacks direct parameter association",
  "path cb_minus_reject_assort: Micro source lacks direct parameter association",
  "path as_plus_shiftvar_mean: Micro source lacks direct parameter association",
  "path as_minus_shiftvar_mean: Micro source lacks direct parameter association",
  "path bt_plus_reject_assort: Micro source lacks direct parameter association",
  "path bt_minus_rewire_mean: Micro source lacks direct parameter association",
  "path cb_plus_count_conn: Micro source lacks direct parameter association",
  "path cb_minus_count_var: Micro source lacks direct parameter association",
  "path as_plus_signflip_assort: Micro source lacks direct parameter association"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "deffuant",
  "indicator_set_sha256": "2bdcf2ab4711e8df29c32538341445f9ed4ca6cad90e57cb0d4f48dd6b49aa15",
  "candidate_paths": [
    {
      "path_id": "cb_plus_accept_homog_var",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_accepted_fraction",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "A larger confidence bound increases the fraction of accepted encounters, leading to more frequent local assimilation and therefore more homogeneous neighborhoods.",
      "mechanistic_explanation": "Increased assimilation reduces opinion differences within connected agent neighborhoods, lowering local opinion standard deviation; reduced local variance then propagates to lower whole-system opinion variance.",
      "falsification_condition": "If macro_opinion_global_variance under plus confidence_bound is not lower than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "cb_minus_accept_heterog_var",
      "parameter": "confidence_bound",
      "intervention_direction": "minus",
      "micro_indicator": "micro_accepted_fraction",
      "meso_indicator": "meso_neighborhood_opinion_variance",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "A smaller confidence bound lowers the accepted fraction, leaving more local opinion differences unresolved and increasing neighborhood heterogeneity.",
      "mechanistic_explanation": "Fewer accepted encounters reduce local assimilation, so neighborhood opinion variance rises; greater local variance contributes to higher whole-system opinion variance.",
      "falsification_condition": "If macro_opinion_global_variance under minus confidence_bound is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "cb_plus_reject_assort",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_rejected_fraction",
      "meso_indicator": "meso_neighborhood_abs_opinion_variance",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "increase",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Increasing confidence_bound reduces rejection-triggered rewiring, which in turn increases local absolute opinion variance and reduces network assortativity.",
      "mechanistic_explanation": "A lower rejection fraction means fewer homophily-biased rewiring events, so local absolute opinion variance increases; higher local variance weakens opinion similarity along edges, decreasing assortativity.",
      "falsification_condition": "If macro_network_assortativity under plus confidence_bound is not lower than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "cb_minus_reject_assort",
      "parameter": "confidence_bound",
      "intervention_direction": "minus",
      "micro_indicator": "micro_rejected_fraction",
      "meso_indicator": "meso_neighborhood_abs_opinion_std",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Decreasing confidence_bound raises rejection-triggered rewiring, which can homogenize local absolute opinions and strengthen assortativity.",
      "mechanistic_explanation": "More rejected encounters lead to more homophily-biased tie replacement, reducing local absolute opinion standard deviation; more homogeneous local neighborhoods yield higher network opinion assortativity.",
      "falsification_condition": "If macro_network_assortativity under minus confidence_bound is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "as_plus_shift_homog_var",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_mean_abs_agent_shift",
      "meso_indicator": "meso_neighborhood_opinion_variance",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Higher assimilation strength increases the magnitude of opinion shifts, which accelerates local convergence and reduces both neighborhood and global opinion variance.",
      "mechanistic_explanation": "Larger accepted updates shrink opinion differences within neighborhoods more quickly, lowering neighborhood opinion variance; lower local variance translates into lower whole-system variance.",
      "falsification_condition": "If macro_opinion_global_variance under plus assimilation_strength is not lower than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "as_minus_shift_frag_conn",
      "parameter": "assimilation_strength",
      "intervention_direction": "minus",
      "micro_indicator": "micro_mean_abs_agent_shift",
      "meso_indicator": "meso_neighborhood_interaction_distance_variance",
      "macro_indicator": "macro_network_largest_component_fraction",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "increase",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Lower assimilation strength reduces opinion updates, preserving heterogeneous interaction distances and weakening global network connectivity.",
      "mechanistic_explanation": "Smaller shifts leave local opinion differences larger, increasing neighborhood interaction distance variance; more variable distances can trigger more rewiring or limit cohesive links, reducing the largest component fraction.",
      "falsification_condition": "If macro_network_largest_component_fraction under minus assimilation_strength is not lower than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "as_plus_shiftvar_mean",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_agent_shift_std",
      "meso_indicator": "meso_neighborhood_abs_opinion_variance",
      "macro_indicator": "macro_opinion_global_mean",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher assimilation strength creates more varied individual updates, enlarging local absolute opinion variance and shifting the global mean upward under the current initial opinion distribution.",
      "mechanistic_explanation": "Increased variance in opinion shifts makes local absolute opinions more dispersed; with a positively skewed initial distribution, this outward movement raises the whole-system mean opinion.",
      "falsification_condition": "If macro_opinion_global_mean under plus assimilation_strength is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "as_minus_shiftvar_mean",
      "parameter": "assimilation_strength",
      "intervention_direction": "minus",
      "micro_indicator": "micro_agent_shift_std",
      "meso_indicator": "meso_neighborhood_opinion_variance",
      "macro_indicator": "macro_opinion_global_mean",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Lower assimilation strength reduces variability in opinion updates, yielding more uniform local opinions and a downward shift in the global mean under the current initial distribution.",
      "mechanistic_explanation": "Decreased shift variance makes neighborhood opinion variance smaller; reduced local dispersion weakens outward mass movement, allowing the global mean to fall relative to baseline.",
      "falsification_condition": "If macro_opinion_global_mean under minus assimilation_strength is not lower than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "bt_plus_backfire_conn",
      "parameter": "backfire_threshold",
      "intervention_direction": "plus",
      "micro_indicator": "micro_backfire_fraction",
      "meso_indicator": "meso_neighborhood_interaction_distance_std",
      "macro_indicator": "macro_network_largest_component_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Raising the backfire threshold reduces repulsive encounters, making local interaction distances more uniform and strengthening the global network component.",
      "mechanistic_explanation": "Fewer backfire events reduce extreme opinion divergence, lowering neighborhood interaction distance standard deviation; more uniform local distances support coherent network connectivity, increasing the largest component fraction.",
      "falsification_condition": "If macro_network_largest_component_fraction under plus backfire_threshold is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "bt_minus_backfire_var",
      "parameter": "backfire_threshold",
      "intervention_direction": "minus",
      "micro_indicator": "micro_backfire_fraction",
      "meso_indicator": "meso_neighborhood_abs_opinion_variance",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Lowering the backfire threshold increases repulsive encounters, which amplifies local absolute opinion differences and raises global variance.",
      "mechanistic_explanation": "More backfire events push connected agents apart, increasing neighborhood absolute opinion variance; this larger local dispersion contributes directly to higher whole-system opinion variance.",
      "falsification_condition": "If macro_opinion_global_variance under minus backfire_threshold is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "bt_plus_reject_assort",
      "parameter": "backfire_threshold",
      "intervention_direction": "plus",
      "micro_indicator": "micro_rejected_fraction",
      "meso_indicator": "meso_neighborhood_opinion_variance",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Increasing the backfire threshold expands the rejection zone, triggering more homophily-biased rewiring that reduces neighborhood variance and raises assortativity.",
      "mechanistic_explanation": "A higher rejection fraction increases adaptive rewiring, which replaces heterogeneous ties with more opinion-similar ones; lower neighborhood opinion variance then strengthens degree-weighted opinion assortativity.",
      "falsification_condition": "If macro_network_assortativity under plus backfire_threshold is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "bt_minus_rewire_mean",
      "parameter": "backfire_threshold",
      "intervention_direction": "minus",
      "micro_indicator": "micro_rewiring_fraction",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_opinion_global_mean",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Lowering the backfire threshold raises both backfire and rejection events, increasing rewiring and decreasing local opinion heterogeneity, which under the current initial conditions lowers the global mean.",
      "mechanistic_explanation": "More rewiring homophily-biasedly sorts agents into opinion-similar neighborhoods, reducing neighborhood opinion standard deviation; this segregation of extreme opinions reduces the whole-system mean.",
      "falsification_condition": "If macro_opinion_global_mean under minus backfire_threshold is not lower than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "cb_plus_count_conn",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_accepted_count",
      "meso_indicator": "meso_neighborhood_interaction_distance_variance",
      "macro_indicator": "macro_network_largest_component_fraction",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "A larger confidence bound increases the total number of accepted interactions, reducing local interaction distance variance and supporting a larger giant component.",
      "mechanistic_explanation": "More accepted encounters reduce the spread of sampled distances within neighborhoods; lower distance variance decreases disruptive rewiring, helping maintain a larger connected component.",
      "falsification_condition": "If macro_network_largest_component_fraction under plus confidence_bound is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "cb_minus_count_var",
      "parameter": "confidence_bound",
      "intervention_direction": "minus",
      "micro_indicator": "micro_accepted_count",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "A smaller confidence bound reduces accepted interactions, increasing local opinion spread and then global variance.",
      "mechanistic_explanation": "Fewer accepted encounters mean less local assimilation, so neighborhood opinion standard deviation rises; higher local dispersion translates into higher whole-system opinion variance.",
      "falsification_condition": "If macro_opinion_global_variance under minus confidence_bound is not higher than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "as_plus_signflip_assort",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_sign_flip_fraction",
      "meso_indicator": "meso_neighborhood_abs_opinion_std",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Stronger assimilation shifts can push more agents across zero, increasing local absolute opinion spread and reducing opinion assortativity.",
      "mechanistic_explanation": "A higher sign-flip fraction reflects larger individual opinion movements, which temporarily increase neighborhood absolute opinion standard deviation; more mixed local signs reduce network assortativity.",
      "falsification_condition": "If macro_network_assortativity under plus assimilation_strength is not lower than baseline at the final simulation segment, the path is falsified."
    },
    {
      "path_id": "bt_plus_backfire_shiftvar",
      "parameter": "backfire_threshold",
      "intervention_direction": "plus",
      "micro_indicator": "micro_backfire_fraction",
      "meso_indicator": "meso_neighborhood_agent_shift_std",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Raising the backfire threshold reduces repulsive shifts, which lowers local shift variability and consequently global variance.",
      "mechanistic_explanation": "Fewer backfire encounters mean less variable repulsive updates, reducing neighborhood agent shift standard deviation; lower local shift variability leads to lower whole-system opinion variance.",
      "falsification_condition": "If macro_opinion_global_variance under plus backfire_threshold is not lower than baseline at the final simulation segment, the path is falsified."
    }
  ],
  "prospective_predictions": [
    {
      "prediction_id": "pred_cb_plus_var_lower",
      "candidate_path_id": "cb_plus_accept_homog_var",
      "prospective_priority": 0,
      "scientific_rationale": "Under plus confidence_bound, accepted fraction should increase, homogenizing neighborhoods and lowering global opinion variance relative to baseline.",
      "falsification_condition": "If macro_opinion_global_variance under plus confidence_bound is not lower than baseline in the final 20 percent of steps, this prediction is falsified."
    },
    {
      "prediction_id": "pred_as_plus_var_lower",
      "candidate_path_id": "as_plus_shift_homog_var",
      "prospective_priority": 0,
      "scientific_rationale": "Higher assimilation strength should increase the magnitude of opinion shifts, accelerate local convergence, and reduce global opinion variance.",
      "falsification_condition": "If macro_opinion_global_variance under plus assimilation_strength is not lower than baseline in the final 20 percent of steps, this prediction is falsified."
    },
    {
      "prediction_id": "pred_bt_plus_conn_higher",
      "candidate_path_id": "bt_plus_backfire_conn",
      "prospective_priority": 0,
      "scientific_rationale": "Increasing backfire threshold should reduce repulsive encounters, stabilize network structure, and increase the largest component fraction.",
      "falsification_condition": "If macro_network_largest_component_fraction under plus backfire_threshold is not higher than baseline in the final 20 percent of steps, this prediction is falsified."
    },
    {
      "prediction_id": "pred_cb_plus_assort_lower",
      "candidate_path_id": "cb_plus_reject_assort",
      "prospective_priority": 0,
      "scientific_rationale": "A larger confidence bound should reduce rejection-triggered rewiring, increasing local absolute variance and thereby lowering network assortativity.",
      "falsification_condition": "If macro_network_assortativity under plus confidence_bound is not lower than baseline in the final 20 percent of steps, this prediction is falsified."
    },
    {
      "prediction_id": "pred_bt_minus_var_higher",
      "candidate_path_id": "bt_minus_backfire_var",
      "prospective_priority": 0,
      "scientific_rationale": "Lowering backfire threshold should raise backfire frequency, increase local absolute opinion variance, and raise global opinion variance.",
      "falsification_condition": "If macro_opinion_global_variance under minus backfire_threshold is not higher than baseline in the final 20 percent of steps, this prediction is falsified."
    },
    {
      "prediction_id": "pred_as_plus_mean_higher",
      "candidate_path_id": "as_plus_shiftvar_mean",
      "prospective_priority": 0,
      "scientific_rationale": "Higher assimilation strength should increase variability in opinion shifts, enlarge local absolute opinion variance, and push the global mean upward under the initial opinion distribution.",
      "falsification_condition": "If macro_opinion_global_mean under plus assimilation_strength is not higher than baseline in the final 20 percent of steps, this prediction is falsified."
    }
  ]
}
