# System

You are constructing an auditable, executable multiscale representation of an emergent phenomenon in an agent-based simulator.

Use only the supplied scenario rules, controllable parameter descriptions, raw-log field schema, generic computation grammar, capacity controls, and structural constraints. Obey the phase-specific schema: indicator generation constructs observables only; path generation may only reference the frozen observable identifiers supplied in its input.

Treat scale as a scientific entity contract, not as a time-window label. Micro denotes individual, interaction, elementary-event, or local primitive processes even when their prevalence is aggregated into a time series. Meso denotes real subset, neighborhood, district, community, cluster, or local-domain organization and must use a supplied grouping or network/spatial structural operation. Macro denotes a whole-system collective state. A rolling window, difference, normalization, or constant rescaling alone never changes scientific scale.

The supplied indicator and candidate-path budgets are capacity controls for this experiment. They are not universal theoretical counts. In indicator generation, construct indicators from the public primitives and generic DSL while satisfying the typed entity_scope and scale rules. In path generation, never create, delete, rename, or modify an indicator.

The computation of every indicator must be a declarative JSON AST from the supplied grammar. Never output Python, source code, or an expression string. Complete candidate paths are semantic hypotheses only; adjacent edges are derived deterministically by the program. Do not claim statistical, causal, or intervention support. Prospective predictions must bind to candidate_path_id before any simulation statistics are observed and include an explicit falsification condition.

Return exactly one JSON object matching the supplied schema.
PHASE A ONLY: construct executable multiscale observables. Do not propose relationships, mechanism paths, or predictions.

# User

Input contract:
{
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
  },
  "phase": "indicator_generation",
  "generic_computation_grammar": {
    "ast_rule": "Every node is a JSON object with an op. No source code or expression strings are allowed.",
    "operators": {
      "abs": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "abs",
          "input": {
            "op": "field",
            "name": "local_similarity"
          }
        }
      },
      "add": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "add",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "binned_entropy": {
        "required": [
          "op",
          "input",
          "axis",
          "bins"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension",
          "bins": "integer in [2,128]"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "binned_entropy",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent",
          "bins": 10
        }
      },
      "clip": {
        "required": [
          "op",
          "input",
          "minimum",
          "maximum"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "minimum": "number",
          "maximum": "number"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "clip",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "minimum": 0.0,
          "maximum": 1.0
        }
      },
      "connected_component_count": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "time-grid AST object"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time]",
        "example": {
          "op": "connected_component_count",
          "input": {
            "op": "field",
            "name": "state_grid"
          }
        }
      },
      "constant": {
        "required": [
          "op",
          "value"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "value": "finite number or boolean"
        },
        "axis_semantics": "not applicable",
        "output": "scalar",
        "example": {
          "op": "constant",
          "value": 0.5
        }
      },
      "correlation": {
        "required": [
          "op",
          "left",
          "right",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "numeric AST object",
          "right": "numeric AST object",
          "axis": "shared named dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "correlation",
          "left": {
            "op": "field",
            "name": "state_opinion"
          },
          "right": {
            "op": "field",
            "name": "agent_shift"
          },
          "axis": "agent"
        }
      },
      "count": {
        "required": [
          "op",
          "input",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "count",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent"
        }
      },
      "distance": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "distance",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "divide": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "divide",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "entropy": {
        "required": [
          "op",
          "input",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "entropy",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent"
        }
      },
      "equal": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "boolean dimensions",
        "example": {
          "op": "equal",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "field": {
        "required": [
          "op",
          "name"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "name": "public raw field name"
        },
        "axis_semantics": "not applicable",
        "output": "raw field dtype and dimensions",
        "example": {
          "op": "field",
          "name": "local_similarity"
        }
      },
      "fraction": {
        "required": [
          "op",
          "input",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "fraction",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent"
        }
      },
      "greater": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "boolean dimensions",
        "example": {
          "op": "greater",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "greater_equal": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "boolean dimensions",
        "example": {
          "op": "greater_equal",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "group_reduce": {
        "required": [
          "op",
          "values",
          "groups",
          "axis",
          "reducer"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "values": "numeric, integer, or boolean AST object",
          "groups": "integer group-membership AST object",
          "axis": "shared entity dimension",
          "reducer": "one of ['count', 'entropy', 'fraction', 'mean', 'std', 'sum', 'variance']"
        },
        "axis_semantics": "required entity axis; replaced by a generic group dimension",
        "output": "numeric dimensions with entity axis replaced by group",
        "example": {
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
          "reducer": "mean"
        }
      },
      "largest_component_fraction": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "time-grid AST object"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time]",
        "example": {
          "op": "largest_component_fraction",
          "input": {
            "op": "field",
            "name": "state_grid"
          }
        }
      },
      "less": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "boolean dimensions",
        "example": {
          "op": "less",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "less_equal": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "boolean dimensions",
        "example": {
          "op": "less_equal",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "log1p": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "log1p",
          "input": {
            "op": "field",
            "name": "local_similarity"
          }
        }
      },
      "mean": {
        "required": [
          "op",
          "input",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "mean",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent"
        }
      },
      "multiply": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "multiply",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "negate": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "negate",
          "input": {
            "op": "field",
            "name": "local_similarity"
          }
        }
      },
      "network_assortativity": {
        "required": [
          "op",
          "values",
          "edges"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "values": "numeric [time,agent] AST",
          "edges": "integer [time,edge,endpoint] AST"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time]",
        "example": {
          "op": "network_assortativity",
          "values": {
            "op": "field",
            "name": "state_opinion"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          }
        }
      },
      "network_component_count": {
        "required": [
          "op",
          "edges",
          "node_count"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "edges": "integer [time,edge,endpoint] AST",
          "node_count": "positive scalar AST"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time]",
        "example": {
          "op": "network_component_count",
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "node_count": {
            "op": "field",
            "name": "agent_count"
          }
        }
      },
      "network_density": {
        "required": [
          "op",
          "edges",
          "node_count"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "edges": "integer [time,edge,endpoint] AST",
          "node_count": "scalar AST"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time] for dynamic edges",
        "example": {
          "op": "network_density",
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "node_count": {
            "op": "field",
            "name": "agent_count"
          }
        }
      },
      "network_largest_component_fraction": {
        "required": [
          "op",
          "edges",
          "node_count"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "edges": "integer [time,edge,endpoint] AST",
          "node_count": "positive scalar AST"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time]",
        "example": {
          "op": "network_largest_component_fraction",
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "node_count": {
            "op": "field",
            "name": "agent_count"
          }
        }
      },
      "network_neighborhood_reduce": {
        "required": [
          "op",
          "values",
          "edges",
          "reducer"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "values": "numeric, integer, or boolean [time,agent] AST",
          "edges": "integer [time,edge,endpoint] AST",
          "reducer": "one of ['count', 'fraction', 'mean', 'std', 'sum', 'variance']"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time,agent] neighborhood statistic",
        "example": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "field",
            "name": "state_opinion"
          },
          "edges": {
            "op": "field",
            "name": "network_edges"
          },
          "reducer": "mean"
        }
      },
      "not_equal": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "boolean dimensions",
        "example": {
          "op": "not_equal",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "quantile": {
        "required": [
          "op",
          "input",
          "axis",
          "q"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension",
          "q": "number in [0,1]"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "quantile",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent",
          "q": 0.5
        }
      },
      "rolling_mean": {
        "required": [
          "op",
          "input",
          "window"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "window": "positive integer"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "rolling_mean",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "window": 3
        }
      },
      "rolling_std": {
        "required": [
          "op",
          "input",
          "window"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "window": "positive integer"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "rolling_std",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "window": 3
        }
      },
      "safe_ratio": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "safe_ratio",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "select": {
        "required": [
          "op",
          "input",
          "axis",
          "index"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension",
          "index": "non-negative integer"
        },
        "axis_semantics": "required; selected and removed from output",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "select",
          "input": {
            "op": "field",
            "name": "agent_position"
          },
          "axis": "coordinate",
          "index": 0
        }
      },
      "spatial_neighbor_similarity": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "time-grid AST object"
        },
        "axis_semantics": "not applicable",
        "output": "numeric [time]",
        "example": {
          "op": "spatial_neighbor_similarity",
          "input": {
            "op": "field",
            "name": "state_grid"
          }
        }
      },
      "sqrt": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "sqrt",
          "input": {
            "op": "field",
            "name": "local_similarity"
          }
        }
      },
      "std": {
        "required": [
          "op",
          "input",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "std",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent"
        }
      },
      "subtract": {
        "required": [
          "op",
          "left",
          "right"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "left": "AST object",
          "right": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "subtract",
          "left": {
            "op": "field",
            "name": "unhappy_count"
          },
          "right": {
            "op": "constant",
            "value": 1
          }
        }
      },
      "sum": {
        "required": [
          "op",
          "input",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "sum",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent"
        }
      },
      "time_difference": {
        "required": [
          "op",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "time_difference",
          "input": {
            "op": "field",
            "name": "local_similarity"
          }
        }
      },
      "variance": {
        "required": [
          "op",
          "input",
          "axis"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "input": "AST object",
          "axis": "named input dimension"
        },
        "axis_semantics": "required; removed from output",
        "output": "numeric input dimensions with axis removed",
        "example": {
          "op": "variance",
          "input": {
            "op": "field",
            "name": "local_similarity"
          },
          "axis": "agent"
        }
      },
      "where": {
        "required": [
          "op",
          "condition",
          "input"
        ],
        "optional": [],
        "types": {
          "op": "string literal",
          "condition": "boolean AST object",
          "input": "AST object"
        },
        "axis_semantics": "not applicable",
        "output": "inherits the validated input dimensions",
        "example": {
          "op": "where",
          "condition": {
            "op": "field",
            "name": "unhappy"
          },
          "input": {
            "op": "field",
            "name": "local_similarity"
          }
        }
      }
    },
    "required_output": "A scalar time series with dimensions [time]."
  },
  "indicator_budget": {
    "micro": 16,
    "meso": 8,
    "macro": 4
  },
  "scale_semantics": {
    "micro": "individual, interaction, elementary event, or local primitive process",
    "meso": "real district, neighborhood, community, cluster, or local-domain organization; an outer mean or sum alone is insufficient",
    "macro": "whole-system collective state or outcome",
    "operators": {
      "elementary_or_local": [
        "correlation",
        "field",
        "select",
        "where"
      ],
      "genuine_meso": [
        "group_reduce",
        "network_neighborhood_reduce"
      ],
      "global_structure": [
        "connected_component_count",
        "largest_component_fraction",
        "network_assortativity",
        "network_component_count",
        "network_density",
        "network_largest_component_fraction",
        "spatial_neighbor_similarity"
      ],
      "trivial_wrappers": [
        "clip",
        "log1p",
        "negate",
        "rolling_mean",
        "rolling_std",
        "sqrt",
        "time_difference"
      ]
    }
  },
  "constraints": [
    "Return exactly 16 Micro, 8 Meso, and 4 Macro executable indicators.",
    "Return no candidate edges, candidate paths, or prospective predictions.",
    "Do not group indicators into arbitrary semantic groups.",
    "Every controllable parameter needs at least one direct Micro association.",
    "Use only public simulator semantics and the supplied raw-log schema.",
    "Do not infer any result from unprovided numerical data."
  ]
}

Output JSON schema:
{
  "$defs": {
    "IndicatorSpec": {
      "additionalProperties": false,
      "description": "One executable observable with no LLM-authored grouping field.",
      "properties": {
        "id": {
          "pattern": "^[a-z][a-z0-9_]{2,63}$",
          "title": "Id",
          "type": "string"
        },
        "semantic_name": {
          "minLength": 3,
          "title": "Semantic Name",
          "type": "string"
        },
        "scientific_definition": {
          "minLength": 12,
          "title": "Scientific Definition",
          "type": "string"
        },
        "phenomenon": {
          "minLength": 3,
          "title": "Phenomenon",
          "type": "string"
        },
        "scale": {
          "enum": [
            "micro",
            "meso",
            "macro"
          ],
          "title": "Scale",
          "type": "string"
        },
        "entity_scope": {
          "enum": [
            "individual",
            "interaction",
            "elementary_event",
            "local_process",
            "neighborhood",
            "district",
            "community",
            "cluster",
            "local_domain",
            "whole_system"
          ],
          "title": "Entity Scope",
          "type": "string"
        },
        "entities": {
          "minLength": 2,
          "title": "Entities",
          "type": "string"
        },
        "source_fields": {
          "items": {
            "type": "string"
          },
          "minItems": 1,
          "title": "Source Fields",
          "type": "array"
        },
        "computation": {
          "additionalProperties": true,
          "title": "Computation",
          "type": "object"
        },
        "temporal_aggregation": {
          "$ref": "#/$defs/TemporalAggregationSpec"
        },
        "parameter_associations": {
          "items": {
            "$ref": "#/$defs/ParameterAssociation"
          },
          "title": "Parameter Associations",
          "type": "array"
        },
        "scientific_rationale": {
          "minLength": 12,
          "title": "Scientific Rationale",
          "type": "string"
        }
      },
      "required": [
        "id",
        "semantic_name",
        "scientific_definition",
        "phenomenon",
        "scale",
        "entity_scope",
        "entities",
        "source_fields",
        "computation",
        "temporal_aggregation",
        "scientific_rationale"
      ],
      "title": "IndicatorSpec",
      "type": "object"
    },
    "ParameterAssociation": {
      "additionalProperties": false,
      "properties": {
        "parameter": {
          "title": "Parameter",
          "type": "string"
        },
        "relationship": {
          "default": "direct",
          "enum": [
            "direct",
            "indirect"
          ],
          "title": "Relationship",
          "type": "string"
        },
        "expected_indicator_direction": {
          "enum": [
            "increase",
            "decrease",
            "mixed",
            "unknown"
          ],
          "title": "Expected Indicator Direction",
          "type": "string"
        },
        "rationale": {
          "minLength": 12,
          "title": "Rationale",
          "type": "string"
        }
      },
      "required": [
        "parameter",
        "expected_indicator_direction",
        "rationale"
      ],
      "title": "ParameterAssociation",
      "type": "object"
    },
    "TemporalAggregationSpec": {
      "additionalProperties": false,
      "properties": {
        "op": {
          "enum": [
            "identity",
            "rolling_mean",
            "rolling_std",
            "difference",
            "cumulative_mean"
          ],
          "title": "Op",
          "type": "string"
        },
        "window": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Window"
        }
      },
      "required": [
        "op"
      ],
      "title": "TemporalAggregationSpec",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "description": "Phase A response; forbidden extras reject paths, edges, and predictions.",
  "properties": {
    "scenario": {
      "title": "Scenario",
      "type": "string"
    },
    "phenomenon": {
      "minLength": 3,
      "title": "Phenomenon",
      "type": "string"
    },
    "indicators": {
      "items": {
        "$ref": "#/$defs/IndicatorSpec"
      },
      "title": "Indicators",
      "type": "array"
    },
    "interpretation_boundary": {
      "minLength": 30,
      "title": "Interpretation Boundary",
      "type": "string"
    }
  },
  "required": [
    "scenario",
    "phenomenon",
    "indicators",
    "interpretation_boundary"
  ],
  "title": "IndicatorGeneration",
  "type": "object"
}

The previous response failed only these schema/executability checks:
[
  "indicator micro_extreme_opinion_fraction: Micro lacks an elementary primitive",
  "indicator meso_neighborhood_opinion_mean: Meso lacks non-trivial organization",
  "indicator meso_neighborhood_opinion_abs_mean: Meso lacks non-trivial organization",
  "indicator meso_neighborhood_assimilation_exposure: network neighborhood mean requires numeric values",
  "indicator meso_neighborhood_assimilation_exposure: Meso lacks non-trivial organization",
  "indicator meso_neighborhood_backfire_exposure: network neighborhood mean requires numeric values",
  "indicator meso_neighborhood_backfire_exposure: Meso lacks non-trivial organization",
  "indicator meso_neighborhood_rewiring_exposure: network neighborhood mean requires numeric values",
  "indicator meso_neighborhood_rewiring_exposure: Meso lacks non-trivial organization",
  "indicator meso_neighborhood_distance_exposure: Meso lacks non-trivial organization",
  "interpretation_boundary must defer temporal and intervention evidence"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "deffuant",
  "phenomenon": "Deffuant opinion dynamics on adaptive degree-eight network",
  "indicators": [
    {
      "id": "micro_opinion_mean",
      "semantic_name": "Mean opinion",
      "scientific_definition": "Cross-agent average of state_opinion at each recorded step.",
      "phenomenon": "Opinion distribution",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Tracks the central tendency of individual opinions as a baseline for convergence."
    },
    {
      "id": "micro_opinion_std",
      "semantic_name": "Opinion standard deviation",
      "scientific_definition": "Cross-agent standard deviation of state_opinion at each recorded step.",
      "phenomenon": "Opinion distribution",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures dispersion across individual opinions, reflecting opinion heterogeneity."
    },
    {
      "id": "micro_opinion_abs_mean",
      "semantic_name": "Mean absolute opinion",
      "scientific_definition": "Cross-agent average of the absolute value of state_opinion at each recorded step.",
      "phenomenon": "Opinion distribution",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "mean",
        "input": {"op": "abs", "input": {"op": "field", "name": "state_opinion"}},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Captures individual opinion extremity without regard to sign."
    },
    {
      "id": "micro_interaction_distance_mean",
      "semantic_name": "Mean interaction distance",
      "scientific_definition": "Cross-agent average absolute opinion distance in sampled interactions at each step.",
      "phenomenon": "Interaction distance distribution",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_distance"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "interaction_distance"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures the typical local opinion distance encountered by agents during interactions."
    },
    {
      "id": "micro_interaction_distance_std",
      "semantic_name": "Interaction distance standard deviation",
      "scientific_definition": "Cross-agent standard deviation of interaction_distance at each step.",
      "phenomenon": "Interaction distance distribution",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_distance"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "interaction_distance"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Captures variability in local opinion distances across sampled interactions."
    },
    {
      "id": "micro_assimilation_rate",
      "semantic_name": "Assimilation encounter rate",
      "scientific_definition": "Fraction of sampled interactions that produce assimilation at each step.",
      "phenomenon": "Assimilation events",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_accepted"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "interaction_accepted"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "parameter_associations": [
        {
          "parameter": "confidence_bound",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "A wider confidence bound makes more sampled opinion distances qualify for assimilation, raising the per-step accepted interaction fraction."
        }
      ],
      "scientific_rationale": "Directly measures the prevalence of the assimilation mechanism at the interaction level."
    },
    {
      "id": "micro_backfire_rate",
      "semantic_name": "Backfire encounter rate",
      "scientific_definition": "Fraction of sampled interactions that trigger repulsive updating at each step.",
      "phenomenon": "Repulsion events",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_backfire"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "interaction_backfire"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "parameter_associations": [
        {
          "parameter": "backfire_threshold",
          "relationship": "direct",
          "expected_indicator_direction": "decrease",
          "rationale": "Raising the backfire threshold shrinks the range of opinion distances that qualify for repulsive updating, reducing the backfire event fraction."
        }
      ],
      "scientific_rationale": "Directly measures the prevalence of repulsive encounter events."
    },
    {
      "id": "micro_rejection_rate",
      "semantic_name": "Rejection encounter rate",
      "scientific_definition": "Fraction of sampled interactions that produce neither assimilation nor repulsion at each step.",
      "phenomenon": "Rejection events",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_rejected"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "interaction_rejected"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures the prevalence of rejected encounters that may drive adaptive rewiring."
    },
    {
      "id": "micro_rewiring_rate",
      "semantic_name": "Rewiring rate",
      "scientific_definition": "Fraction of sampled interactions in which the focal tie is successfully rewired at each step.",
      "phenomenon": "Adaptive rewiring events",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "sampled ties undergoing rewiring",
      "source_fields": ["edge_rewired"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "edge_rewired"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Tracks the frequency of local network restructuring from rejected or backfire encounters."
    },
    {
      "id": "micro_agent_shift_mean",
      "semantic_name": "Mean signed opinion shift",
      "scientific_definition": "Cross-agent average of signed opinion update agent_shift at each step.",
      "phenomenon": "Opinion updating",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "agent_shift"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measuring signed shifts reveals whether updates are biased toward one opinion direction across individuals."
    },
    {
      "id": "micro_agent_shift_abs_mean",
      "semantic_name": "Mean absolute opinion shift",
      "scientific_definition": "Cross-agent average of the absolute value of agent_shift at each step.",
      "phenomenon": "Opinion updating",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "mean",
        "input": {"op": "abs", "input": {"op": "field", "name": "agent_shift"}},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "parameter_associations": [
        {
          "parameter": "assimilation_strength",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Stronger assimilation applies a larger fraction of the partner difference during accepted encounters, increasing the magnitude of individual opinion updates."
        }
      ],
      "scientific_rationale": "Captures the typical magnitude of individual opinion change regardless of direction."
    },
    {
      "id": "micro_agent_shift_std",
      "semantic_name": "Opinion shift standard deviation",
      "scientific_definition": "Cross-agent standard deviation of agent_shift at each step.",
      "phenomenon": "Opinion updating",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "agent_shift"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures heterogeneity in individual opinion updates across the population."
    },
    {
      "id": "micro_accepted_distance_mean",
      "semantic_name": "Mean accepted interaction distance",
      "scientific_definition": "Cross-agent average of interaction_distance only for interactions with interaction_accepted true.",
      "phenomenon": "Assimilation event distance",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "accepted sampled interactions",
      "source_fields": ["interaction_accepted", "interaction_distance"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "where",
          "condition": {"op": "field", "name": "interaction_accepted"},
          "input": {"op": "field", "name": "interaction_distance"}
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "parameter_associations": [
        {
          "parameter": "confidence_bound",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "A larger confidence bound permits assimilation at larger opinion distances, increasing the average distance among accepted interactions."
        }
      ],
      "scientific_rationale": "Characterizes the distance range over which assimilation actually occurs."
    },
    {
      "id": "micro_backfire_distance_mean",
      "semantic_name": "Mean backfire interaction distance",
      "scientific_definition": "Cross-agent average of interaction_distance only for interactions with interaction_backfire true.",
      "phenomenon": "Repulsion event distance",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "backfire sampled interactions",
      "source_fields": ["interaction_backfire", "interaction_distance"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "where",
          "condition": {"op": "field", "name": "interaction_backfire"},
          "input": {"op": "field", "name": "interaction_distance"}
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "parameter_associations": [
        {
          "parameter": "backfire_threshold",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Raising the repulsion threshold removes lower-distance backfire cases, so the average distance among remaining backfire events increases."
        }
      ],
      "scientific_rationale": "Captures the opinion distance range where repulsive updating actually occurs."
    },
    {
      "id": "micro_sign_flip_rate",
      "semantic_name": "Sign flip rate",
      "scientific_definition": "Fraction of individual agents whose opinion update crosses zero at each step.",
      "phenomenon": "Sign crossing events",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "individual agents",
      "source_fields": ["sign_flip"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "sign_flip"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Detects whether updates move individuals across the neutral opinion boundary."
    },
    {
      "id": "micro_extreme_opinion_fraction",
      "semantic_name": "Extreme opinion fraction",
      "scientific_definition": "Fraction of agents with absolute opinion at least 0.75 at each step.",
      "phenomenon": "Extreme opinion prevalence",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["extreme_agent_count", "agent_count"],
      "computation": {
        "op": "divide",
        "left": {"op": "field", "name": "extreme_agent_count"},
        "right": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures the prevalence of individual agents holding strongly non-neutral opinions."
    },
    {
      "id": "meso_neighborhood_opinion_mean",
      "semantic_name": "Mean neighborhood mean opinion",
      "scientific_definition": "Cross-agent average of the mean state_opinion among each agent's network neighbors at each step.",
      "phenomenon": "Neighborhood opinion organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "state_opinion"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Uses the current network structure to summarize local opinion consensus within neighborhoods rather than the whole system."
    },
    {
      "id": "meso_neighborhood_opinion_std",
      "semantic_name": "Neighborhood mean opinion standard deviation",
      "scientific_definition": "Cross-agent standard deviation of neighborhood mean state_opinion at each step.",
      "phenomenon": "Neighborhood opinion organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "std",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "state_opinion"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Captures heterogeneity across neighborhoods in their local average opinion."
    },
    {
      "id": "meso_neighborhood_opinion_abs_mean",
      "semantic_name": "Mean neighborhood absolute opinion",
      "scientific_definition": "Cross-agent average of the neighborhood mean absolute state_opinion at each step.",
      "phenomenon": "Neighborhood opinion organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "abs", "input": {"op": "field", "name": "state_opinion"}},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures typical neighborhood-level opinion extremity without regard to opinion sign."
    },
    {
      "id": "meso_neighborhood_opinion_diversity",
      "semantic_name": "Mean within-neighborhood opinion diversity",
      "scientific_definition": "Cross-agent average of the within-neighborhood standard deviation of state_opinion at each step.",
      "phenomenon": "Neighborhood opinion organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "state_opinion"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "std"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Quantifies how diverse opinions are within local network neighborhoods."
    },
    {
      "id": "meso_neighborhood_assimilation_exposure",
      "semantic_name": "Neighborhood assimilation exposure",
      "scientific_definition": "Cross-agent average of the neighborhood mean of interaction_accepted at each step.",
      "phenomenon": "Local assimilation organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["interaction_accepted", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_accepted"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures whether accepted interactions cluster within particular network neighborhoods."
    },
    {
      "id": "meso_neighborhood_backfire_exposure",
      "semantic_name": "Neighborhood backfire exposure",
      "scientific_definition": "Cross-agent average of the neighborhood mean of interaction_backfire at each step.",
      "phenomenon": "Local repulsion organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["interaction_backfire", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_backfire"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures whether repulsive encounters cluster within particular network neighborhoods."
    },
    {
      "id": "meso_neighborhood_rewiring_exposure",
      "semantic_name": "Neighborhood rewiring exposure",
      "scientific_definition": "Cross-agent average of the neighborhood mean of edge_rewired at each step.",
      "phenomenon": "Local rewiring organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["edge_rewired", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "edge_rewired"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures whether adaptive rewiring events cluster within particular network neighborhoods."
    },
    {
      "id": "meso_neighborhood_distance_exposure",
      "semantic_name": "Neighborhood interaction distance exposure",
      "scientific_definition": "Cross-agent average of the neighborhood mean of interaction_distance at each step.",
      "phenomenon": "Local distance organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "current network neighborhoods",
      "source_fields": ["interaction_distance", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_distance"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures whether sampled opinion distances cluster within particular network neighborhoods."
    },
    {
      "id": "macro_opinion_entropy",
      "semantic_name": "Opinion binned entropy",
      "scientific_definition": "Shannon entropy of state_opinion values across agents with 20 equal-width bins at each step.",
      "phenomenon": "Whole-system opinion distribution",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "all agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "binned_entropy",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent",
        "bins": 20
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "A system-level entropy measure responds to consensus or multiple opinion clusters without assuming a particular distribution."
    },
    {
      "id": "macro_network_assortativity",
      "semantic_name": "Opinion assortativity",
      "scientific_definition": "Whole-network correlation of state_opinion between connected agent pairs at each step.",
      "phenomenon": "Opinion-topology alignment",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "network edges and agent opinions",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "network_assortativity",
        "values": {"op": "field", "name": "state_opinion"},
        "edges": {"op": "field", "name": "network_edges"}
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Whole-system assortativity captures whether similarly opinionated agents connect, a signature of homophilous network structure."
    },
    {
      "id": "macro_network_component_count",
      "semantic_name": "Network component count",
      "scientific_definition": "Number of connected components in the current undirected network at each step.",
      "phenomenon": "Whole-system network fragmentation",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "network components",
      "source_fields": ["network_edges", "agent_count"],
      "computation": {
        "op": "network_component_count",
        "edges": {"op": "field", "name": "network_edges"},
        "node_count": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Component count tracks whole-system fragmentation from adaptive rewiring."
    },
    {
      "id": "macro_network_largest_component_fraction",
      "semantic_name": "Largest component fraction",
      "scientific_definition": "Fraction of all agents in the largest connected component of the current network at each step.",
      "phenomenon": "Whole-system network connectivity",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "largest network component",
      "source_fields": ["network_edges", "agent_count"],
      "computation": {
        "op": "network_largest_component_fraction",
        "edges": {"op": "field", "name": "network_edges"},
        "node_count": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity"},
      "scientific_rationale": "Measures global connectivity retention and the breadth of the largest connected component."
    }
  ],
  "interpretation_boundary": "Indicators are computed solely from raw-log fields and are observables only. They do not imply statistical, causal, or intervention support, and scale labels refer to the target level of organization rather than to dynamic mechanisms."
}
