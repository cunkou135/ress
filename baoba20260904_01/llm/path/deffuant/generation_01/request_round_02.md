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
  "path cp_confidence_plus_rejected_neighb_std_assort: Micro source lacks direct parameter association",
  "path cp_confidence_plus_opinion_std_neighb_std_assort: Micro source lacks direct parameter association",
  "path cp_confidence_plus_rewiring_interact_std_component: Micro source lacks direct parameter association",
  "path cp_assimilation_plus_shift_std_neighb_shift_std_assort: Micro source lacks direct parameter association",
  "path cp_assimilation_plus_opinion_std_neighb_std_component: Micro source lacks direct parameter association",
  "path cp_backfire_plus_rejected_neighb_var_assort: Micro source lacks direct parameter association",
  "path cp_backfire_plus_extreme_abs_std_global_mean: Micro source lacks direct parameter association",
  "path cp_confidence_plus_p25_neighb_var_global_mean: Micro source lacks direct parameter association"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "deffuant",
  "indicator_set_sha256": "2bdcf2ab4711e8df29c32538341445f9ed4ca6cad90e57cb0d4f48dd6b49aa15",
  "candidate_paths": [
    {
      "path_id": "cp_confidence_plus_accepted_neighb_std_global_var",
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
      "scientific_rationale": "Larger confidence_bound increases accepted fraction, reducing neighborhood opinion heterogeneity and lowering global variance.",
      "mechanistic_explanation": "More encounters fall within the assimilation window, so nearby agents converge more often. This reduces the standard deviation of opinions inside each neighborhood, and lower local spread translates into lower whole-system opinion variance.",
      "falsification_condition": "If simulated confidence_bound plus does not increase micro_accepted_fraction or does not reduce meso_neighborhood_opinion_std, the path is falsified."
    },
    {
      "path_id": "cp_confidence_plus_accepted_neighb_var_global_var",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_accepted_fraction",
      "meso_indicator": "meso_neighborhood_opinion_variance",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "More accepted interactions under plus confidence_bound reduce neighborhood opinion variance and thus global variance.",
      "mechanistic_explanation": "A larger confidence bound allows assimilation over larger distances, reducing local opinion variance. Lower local variance propagates to lower whole-system opinion variance.",
      "falsification_condition": "If plus confidence_bound does not increase micro_accepted_fraction or does not decrease meso_neighborhood_opinion_variance, the path is falsified."
    },
    {
      "path_id": "cp_confidence_plus_rejected_neighb_std_assort",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_rejected_fraction",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Increasing confidence_bound decreases rejected encounters, lowering local opinion heterogeneity and raising network assortativity.",
      "mechanistic_explanation": "Rejected interactions leave moderate-distance pairs unchanged, maintaining neighborhood opinion spread. With fewer rejections, local opinion variation drops, making connected agents more similar and increasing degree-weighted assortativity.",
      "falsification_condition": "If micro_rejected_fraction does not decrease or meso_neighborhood_opinion_std does not decrease under plus confidence_bound, the path is falsified."
    },
    {
      "path_id": "cp_confidence_plus_opinion_std_neighb_std_assort",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_opinion_std",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Larger confidence_bound reduces individual opinion dispersion, lowering neighborhood dispersion and increasing network assortativity.",
      "mechanistic_explanation": "As agents converge, the across-agent standard deviation falls, which reduces the typical spread within neighborhoods. More similar connected agents increase network opinion assortativity.",
      "falsification_condition": "If micro_opinion_std does not decrease or macro_network_assortativity does not increase under plus confidence_bound, the path is falsified."
    },
    {
      "path_id": "cp_confidence_plus_rewiring_interact_std_component",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_rewiring_fraction",
      "meso_indicator": "meso_neighborhood_interaction_distance_std",
      "macro_indicator": "macro_network_largest_component_fraction",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "increase",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Larger confidence_bound reduces adaptive rewiring, leaving local interaction distances more heterogeneous and lowering largest component fraction.",
      "mechanistic_explanation": "Fewer rejected or backfire encounters reduce rewiring events. Without rewiring, local neighborhoods do not become homophilically sorted, so interaction distances vary more and network cohesion weakens, shrinking the largest component.",
      "falsification_condition": "If micro_rewiring_fraction does not decrease or meso_neighborhood_interaction_distance_std does not increase under plus confidence_bound, the path is falsified."
    },
    {
      "path_id": "cp_confidence_plus_accepted_interact_std_component",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_accepted_fraction",
      "meso_indicator": "meso_neighborhood_interaction_distance_std",
      "macro_indicator": "macro_network_largest_component_fraction",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher confidence_bound increases assimilation, reducing local interaction-distance variability and increasing network cohesion.",
      "mechanistic_explanation": "As agents assimilate, opinion gaps between neighbors shrink, lowering the standard deviation of sampled interaction distances within neighborhoods. This homogenization strengthens ties and enlarges the largest connected component.",
      "falsification_condition": "If micro_accepted_fraction does not increase or macro_network_largest_component_fraction does not increase under plus confidence_bound, the path is falsified."
    },
    {
      "path_id": "cp_assimilation_plus_shift_neighb_std_global_var",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_mean_abs_agent_shift",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Higher assimilation_strength increases mean absolute opinion shifts, rapidly reducing neighborhood opinion dispersion and global variance.",
      "mechanistic_explanation": "Stronger assimilation applies a larger fraction of partner distance, producing larger opinion adjustments. These larger shifts reduce opinion differences within neighborhoods faster, lowering local standard deviation and eventually whole-system variance.",
      "falsification_condition": "If micro_mean_abs_agent_shift does not increase or macro_opinion_global_variance does not decrease under plus assimilation_strength, the path is falsified."
    },
    {
      "path_id": "cp_assimilation_plus_shift_neighb_var_global_var",
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
      "scientific_rationale": "Stronger assimilation shifts reduce neighborhood opinion variance, leading to lower global variance.",
      "mechanistic_explanation": "Larger opinion updates accelerate local convergence, decreasing the variance of opinions within neighborhoods. Lower local variance propagates to lower whole-system variance.",
      "falsification_condition": "If micro_mean_abs_agent_shift does not increase or meso_neighborhood_opinion_variance does not decrease under plus assimilation_strength, the path is falsified."
    },
    {
      "path_id": "cp_assimilation_plus_shift_std_neighb_shift_std_assort",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_agent_shift_std",
      "meso_indicator": "meso_neighborhood_agent_shift_std",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "increase",
      "expected_meso_response": "increase",
      "expected_macro_response": "increase",
      "scientific_rationale": "Stronger assimilation_strength increases variability of opinion shifts, increasing neighborhood shift variability and network opinion assortativity.",
      "mechanistic_explanation": "Larger assimilation scales opinion shifts by partner distance, producing more variable individual updates. This greater local shift heterogeneity is accompanied by stronger local opinion sorting, increasing degree-weighted assortativity.",
      "falsification_condition": "If micro_agent_shift_std does not increase or macro_network_assortativity does not increase under plus assimilation_strength, the path is falsified."
    },
    {
      "path_id": "cp_assimilation_plus_shift_neighb_std_assort",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_mean_abs_agent_shift",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher assimilation_strength reduces neighborhood opinion spread, increasing similarity among connected agents and raising assortativity.",
      "mechanistic_explanation": "Larger opinion adjustments accelerate local convergence, decreasing the standard deviation of opinions within neighborhoods. More homogeneous neighborhoods produce stronger opinion assortativity on the network.",
      "falsification_condition": "If micro_mean_abs_agent_shift does not increase or macro_network_assortativity does not increase under plus assimilation_strength, the path is falsified."
    },
    {
      "path_id": "cp_assimilation_plus_shift_interact_std_component",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_mean_abs_agent_shift",
      "meso_indicator": "meso_neighborhood_interaction_distance_std",
      "macro_indicator": "macro_network_largest_component_fraction",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Stronger assimilation_strength reduces local interaction-distance variability, enhancing network cohesion and largest component fraction.",
      "mechanistic_explanation": "Larger shifts bring neighbor opinions closer, reducing the spread of sampled distances within neighborhoods. Lower local distance variability strengthens cohesive ties and enlarges the largest connected component.",
      "falsification_condition": "If micro_mean_abs_agent_shift does not increase or macro_network_largest_component_fraction does not increase under plus assimilation_strength, the path is falsified."
    },
    {
      "path_id": "cp_assimilation_plus_opinion_std_neighb_std_component",
      "parameter": "assimilation_strength",
      "intervention_direction": "plus",
      "micro_indicator": "micro_opinion_std",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_network_largest_component_fraction",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher assimilation_strength reduces global opinion dispersion and neighborhood heterogeneity, increasing largest component fraction.",
      "mechanistic_explanation": "Stronger assimilation reduces both across-agent opinion standard deviation and within-neighborhood standard deviation. Lower local heterogeneity supports stronger network connectivity, increasing the largest component fraction.",
      "falsification_condition": "If micro_opinion_std does not decrease or macro_network_largest_component_fraction does not increase under plus assimilation_strength, the path is falsified."
    },
    {
      "path_id": "cp_backfire_plus_backfire_neighb_std_global_var",
      "parameter": "backfire_threshold",
      "intervention_direction": "plus",
      "micro_indicator": "micro_backfire_fraction",
      "meso_indicator": "meso_neighborhood_opinion_std",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Raising backfire_threshold decreases backfire fraction, lowering neighborhood opinion spread and global variance.",
      "mechanistic_explanation": "Fewer sufficiently distant encounters trigger repulsive updates, so neighbors are less likely to be pushed apart. This reduces local opinion standard deviation, which lowers whole-system opinion variance.",
      "falsification_condition": "If micro_backfire_fraction does not decrease or macro_opinion_global_variance does not decrease under plus backfire_threshold, the path is falsified."
    },
    {
      "path_id": "cp_backfire_plus_backfire_neighb_var_global_var",
      "parameter": "backfire_threshold",
      "intervention_direction": "plus",
      "micro_indicator": "micro_backfire_fraction",
      "meso_indicator": "meso_neighborhood_opinion_variance",
      "macro_indicator": "macro_opinion_global_variance",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "increase",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "decrease",
      "scientific_rationale": "Fewer backfire events under plus backfire_threshold reduce local opinion variance and global variance.",
      "mechanistic_explanation": "With a higher threshold, fewer encounters produce repulsive updates, so neighborhood opinion variance declines. Lower local variance translates into lower whole-system variance.",
      "falsification_condition": "If micro_backfire_fraction does not decrease or meso_neighborhood_opinion_variance does not decrease under plus backfire_threshold, the path is falsified."
    },
    {
      "path_id": "cp_backfire_plus_rejected_neighb_var_assort",
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
      "scientific_rationale": "Higher backfire_threshold converts some backfire encounters into rejections, reducing local opinion variance and increasing network assortativity.",
      "mechanistic_explanation": "Repulsive events that would separate distant opinions become neutral rejections, so neighborhood opinion variance declines. Lower local variance makes connected agents more similar, increasing degree-weighted opinion assortativity.",
      "falsification_condition": "If micro_rejected_fraction does not increase or meso_neighborhood_opinion_variance does not decrease or macro_network_assortativity does not increase under plus backfire_threshold, the path is falsified."
    },
    {
      "path_id": "cp_backfire_plus_backfire_interact_std_assort",
      "parameter": "backfire_threshold",
      "intervention_direction": "plus",
      "micro_indicator": "micro_backfire_fraction",
      "meso_indicator": "meso_neighborhood_interaction_distance_std",
      "macro_indicator": "macro_network_assortativity",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Higher backfire_threshold reduces repulsive spreading, lowering interaction-distance variability and increasing opinion assortativity.",
      "mechanistic_explanation": "Fewer backfire events mean less repulsion between distant agents, reducing local variation in interaction distances. Lower distance variability indicates more homophilic neighborhoods, increasing network opinion assortativity.",
      "falsification_condition": "If micro_backfire_fraction does not decrease or macro_network_assortativity does not increase under plus backfire_threshold, the path is falsified."
    },
    {
      "path_id": "cp_backfire_plus_extreme_abs_std_global_mean",
      "parameter": "backfire_threshold",
      "intervention_direction": "plus",
      "micro_indicator": "micro_extreme_agent_fraction",
      "meso_indicator": "meso_neighborhood_abs_opinion_std",
      "macro_indicator": "macro_opinion_global_mean",
      "micro_to_meso_expected_direction": "increase",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "decrease",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Raising backfire_threshold reduces extreme opinion generation, lowering absolute-opinion neighborhood heterogeneity and increasing global mean opinion.",
      "mechanistic_explanation": "With fewer backfire events, agents are less likely to be pushed to extreme opinions, reducing the fraction of extreme agents. Lower extreme prevalence decreases neighborhood absolute-opinion standard deviation, shifting the whole-system mean upward.",
      "falsification_condition": "If micro_extreme_agent_fraction does not decrease or macro_opinion_global_mean does not increase under plus backfire_threshold, the path is falsified."
    },
    {
      "path_id": "cp_confidence_plus_p25_neighb_var_global_mean",
      "parameter": "confidence_bound",
      "intervention_direction": "plus",
      "micro_indicator": "micro_opinion_p25",
      "meso_indicator": "meso_neighborhood_opinion_variance",
      "macro_indicator": "macro_opinion_global_mean",
      "micro_to_meso_expected_direction": "decrease",
      "meso_to_macro_expected_direction": "decrease",
      "expected_micro_response": "increase",
      "expected_meso_response": "decrease",
      "expected_macro_response": "increase",
      "scientific_rationale": "Larger confidence_bound raises the lower opinion quartile, reducing neighborhood opinion variance and increasing global mean opinion.",
      "mechanistic_explanation": "More assimilation moves lower-opinion agents toward the center, increasing the 25th percentile. This reduces local variance as opinions become more similar, and the reduction in low-opinion mass raises the whole-system mean.",
      "falsification_condition": "If micro_opinion_p25 does not increase or macro_opinion_global_mean does not increase under plus confidence_bound, the path is falsified."
    }
  ],
  "prospective_predictions": [
    {
      "prediction_id": "pred_confidence_plus_consensus_variance",
      "candidate_path_id": "cp_confidence_plus_accepted_neighb_std_global_var",
      "prospective_priority": 0,
      "scientific_rationale": "Increased confidence bound should raise assimilation and reduce both local and global opinion dispersion.",
      "falsification_condition": "Falsified if plus confidence_bound simulations do not show increased micro_accepted_fraction and decreased meso_neighborhood_opinion_std and macro_opinion_global_variance."
    },
    {
      "prediction_id": "pred_assimilation_strength_plus_local_convergence",
      "candidate_path_id": "cp_assimilation_plus_shift_neighb_std_global_var",
      "prospective_priority": 1,
      "scientific_rationale": "Higher assimilation strength should strengthen local convergence and reduce global opinion variance.",
      "falsification_condition": "Falsified if plus assimilation_strength does not increase micro_mean_abs_agent_shift or does not decrease macro_opinion_global_variance."
    },
    {
      "prediction_id": "pred_backfire_threshold_plus_variance_reduction",
      "candidate_path_id": "cp_backfire_plus_backfire_neighb_std_global_var",
      "prospective_priority": 2,
      "scientific_rationale": "Raising backfire threshold should reduce repulsion and lower opinion variance across scales.",
      "falsification_condition": "Falsified if plus backfire_threshold does not decrease micro_backfire_fraction or does not decrease macro_opinion_global_variance."
    },
    {
      "prediction_id": "pred_confidence_plus_rejected_assortativity",
      "candidate_path_id": "cp_confidence_plus_rejected_neighb_std_assort",
      "prospective_priority": 3,
      "scientific_rationale": "Higher confidence bound should reduce rejections and increase network opinion assortativity.",
      "falsification_condition": "Falsified if plus confidence_bound does not decrease micro_rejected_fraction or does not increase macro_network_assortativity."
    },
    {
      "prediction_id": "pred_assimilation_strength_plus_shift_variability_assort",
      "candidate_path_id": "cp_assimilation_plus_shift_std_neighb_shift_std_assort",
      "prospective_priority": 4,
      "scientific_rationale": "Stronger assimilation should increase shift variability and network assortativity.",
      "falsification_condition": "Falsified if plus assimilation_strength does not increase micro_agent_shift_std or does not increase macro_network_assortativity."
    },
    {
      "prediction_id": "pred_backfire_threshold_plus_rejected_assortativity",
      "candidate_path_id": "cp_backfire_plus_rejected_neighb_var_assort",
      "prospective_priority": 5,
      "scientific_rationale": "Higher backfire threshold should reduce repulsive backfire events, lowering local opinion variance and increasing network assortativity.",
      "falsification_condition": "Falsified if plus backfire_threshold does not increase micro_rejected_fraction or does not decrease meso_neighborhood_opinion_variance or does not increase macro_network_assortativity."
    }
  ]
}
