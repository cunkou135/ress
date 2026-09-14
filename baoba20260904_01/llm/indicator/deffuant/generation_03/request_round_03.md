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
  "indicator meso_neigh_opinion_distance_corr: Meso lacks non-trivial organization"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "deffuant",
  "phenomenon": "Opinion assimilation and adaptive rewiring coevolution",
  "indicators": [
    {
      "id": "mic_mean_opinion",
      "semantic_name": "Mean opinion",
      "scientific_definition": "Time series of average agent opinion before each step update.",
      "phenomenon": "opinion dynamics",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Mean opinion tracks the central tendency of individual opinion states over time."
    },
    {
      "id": "mic_opinion_std",
      "semantic_name": "Opinion standard deviation",
      "scientific_definition": "Time series of standard deviation of opinions across agents before each step.",
      "phenomenon": "opinion heterogeneity",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Opinion standard deviation measures the dispersion of individual opinion states across the population."
    },
    {
      "id": "mic_extreme_opinion_fraction",
      "semantic_name": "Extreme opinion fraction",
      "scientific_definition": "Fraction of agents with absolute opinion at least 0.75 before each step.",
      "phenomenon": "opinion polarization",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "greater_equal",
          "left": {"op": "abs", "input": {"op": "field", "name": "state_opinion"}},
          "right": {"op": "constant", "value": 0.75}
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Extreme opinion fraction tracks the prevalence of individuals holding strongly polarized opinion states."
    },
    {
      "id": "mic_mean_interaction_distance",
      "semantic_name": "Mean interaction opinion distance",
      "scientific_definition": "Average absolute opinion distance in sampled neighbour encounters at each step.",
      "phenomenon": "interaction distance",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled interactions",
      "source_fields": ["interaction_distance"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "interaction_distance"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Mean interaction distance characterizes the typical opinion separation in sampled social encounters."
    },
    {
      "id": "mic_interaction_distance_std",
      "semantic_name": "Interaction distance standard deviation",
      "scientific_definition": "Standard deviation of absolute opinion distances in sampled interactions across agents.",
      "phenomenon": "interaction distance heterogeneity",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled interactions",
      "source_fields": ["interaction_distance"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "interaction_distance"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Interaction distance standard deviation captures variability in opinion separation across sampled encounters."
    },
    {
      "id": "mic_interaction_distance_median",
      "semantic_name": "Median interaction opinion distance",
      "scientific_definition": "Median absolute opinion distance across sampled interactions at each step.",
      "phenomenon": "interaction distance",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled interactions",
      "source_fields": ["interaction_distance"],
      "computation": {
        "op": "quantile",
        "input": {"op": "field", "name": "interaction_distance"},
        "axis": "agent",
        "q": 0.5
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Median interaction distance is a robust central measure of opinion separation in sampled encounters."
    },
    {
      "id": "mic_accepted_fraction",
      "semantic_name": "Assimilation encounter fraction",
      "scientific_definition": "Fraction of sampled interactions that qualify for assimilation because opinion distance is within the confidence bound.",
      "phenomenon": "opinion assimilation",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled interactions",
      "source_fields": ["interaction_accepted"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "interaction_accepted"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "confidence_bound",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "A larger confidence bound permits more sampled opinion distances to satisfy the assimilation condition."
        }
      ],
      "scientific_rationale": "The assimilation encounter fraction tracks how often sampled interactions are accepted for opinion convergence."
    },
    {
      "id": "mic_backfire_fraction",
      "semantic_name": "Backfire encounter fraction",
      "scientific_definition": "Fraction of sampled interactions that trigger repulsive updating due to opinion distance at least the backfire threshold.",
      "phenomenon": "opinion repulsion",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled interactions",
      "source_fields": ["interaction_backfire"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "interaction_backfire"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "backfire_threshold",
          "relationship": "direct",
          "expected_indicator_direction": "decrease",
          "rationale": "Raising the backfire threshold makes it harder for sampled opinion distances to trigger repulsive updating."
        }
      ],
      "scientific_rationale": "The backfire encounter fraction tracks the incidence of repulsive interaction events."
    },
    {
      "id": "mic_rejected_fraction",
      "semantic_name": "Rejected encounter fraction",
      "scientific_definition": "Fraction of sampled interactions that produce neither assimilation nor repulsion.",
      "phenomenon": "interaction rejection",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled interactions",
      "source_fields": ["interaction_rejected"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "interaction_rejected"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "The rejected encounter fraction tracks how often sampled interactions are neither assimilative nor repulsive."
    },
    {
      "id": "mic_rewired_fraction",
      "semantic_name": "Adaptive rewiring event fraction",
      "scientific_definition": "Fraction of sampled ties that are successfully replaced after rejected or backfire encounters.",
      "phenomenon": "adaptive rewiring",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled interactions",
      "source_fields": ["edge_rewired"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "edge_rewired"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "The rewiring event fraction measures how often rejected or backfire encounters replace the sampled social tie."
    },
    {
      "id": "mic_mean_abs_agent_shift",
      "semantic_name": "Mean absolute opinion update",
      "scientific_definition": "Average absolute signed opinion update applied to agents at each step.",
      "phenomenon": "opinion update magnitude",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "abs",
          "input": {"op": "field", "name": "agent_shift"}
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "assimilation_strength",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Larger assimilation strength increases the magnitude of accepted opinion updates, raising mean absolute shift."
        }
      ],
      "scientific_rationale": "Mean absolute opinion update captures the average amount of opinion change experienced by individual agents."
    },
    {
      "id": "mic_agent_shift_std",
      "semantic_name": "Opinion update standard deviation",
      "scientific_definition": "Standard deviation of signed opinion updates across agents at each step.",
      "phenomenon": "opinion update heterogeneity",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "agent_shift"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Opinion update standard deviation measures heterogeneity in individual opinion changes across the population."
    },
    {
      "id": "mic_sign_flip_fraction",
      "semantic_name": "Opinion sign flip fraction",
      "scientific_definition": "Fraction of agents whose opinion update crosses opinion zero at each step.",
      "phenomenon": "opinion sign crossing",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "update events",
      "source_fields": ["sign_flip"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "sign_flip"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Sign flip fraction tracks how often individual opinion updates move an agent across the neutral opinion point."
    },
    {
      "id": "mic_positive_shift_fraction",
      "semantic_name": "Positive opinion update fraction",
      "scientific_definition": "Fraction of agents with a positive signed opinion update at each step.",
      "phenomenon": "opinion update direction",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "update events",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "greater",
          "left": {"op": "field", "name": "agent_shift"},
          "right": {"op": "constant", "value": 0}
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Positive update fraction indicates the proportion of agents whose opinion moves in the positive direction at each step."
    },
    {
      "id": "mic_opinion_shift_correlation",
      "semantic_name": "Opinion-update correlation",
      "scientific_definition": "Correlation across agents between current opinion and signed opinion update at each step.",
      "phenomenon": "opinion-update coupling",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents",
      "source_fields": ["state_opinion", "agent_shift"],
      "computation": {
        "op": "correlation",
        "left": {"op": "field", "name": "state_opinion"},
        "right": {"op": "field", "name": "agent_shift"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Opinion-update correlation reveals how individual opinion states co-vary with immediate opinion changes across agents."
    },
    {
      "id": "mic_opinion_binned_entropy",
      "semantic_name": "Opinion distribution entropy",
      "scientific_definition": "Binned entropy of opinion states across agents before each step update.",
      "phenomenon": "opinion diversity",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "binned_entropy",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent",
        "bins": 12
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Binned opinion entropy summarizes the diversity of individual opinion states across the population."
    },
    {
      "id": "meso_neigh_mean_opinion_std",
      "semantic_name": "Neighborhood mean opinion heterogeneity",
      "scientific_definition": "Standard deviation across network neighborhoods of average neighbor opinion at each step.",
      "phenomenon": "local opinion differentiation",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
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
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Heterogeneity of neighborhood mean opinions reveals differentiation among local opinion domains."
    },
    {
      "id": "meso_neigh_extreme_opinion_std",
      "semantic_name": "Neighborhood extreme opinion prevalence heterogeneity",
      "scientific_definition": "Standard deviation across network neighborhoods of the fraction of neighbors with absolute opinion at least 0.75.",
      "phenomenon": "local polarization organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "std",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "greater_equal",
            "left": {"op": "abs", "input": {"op": "field", "name": "state_opinion"}},
            "right": {"op": "constant", "value": 0.75}
          },
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "fraction"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Dispersion of neighborhood extreme opinion prevalence measures how unevenly polarized opinions are organized across local social domains."
    },
    {
      "id": "meso_neigh_accepted_std",
      "semantic_name": "Neighborhood assimilation interaction variability",
      "scientific_definition": "Standard deviation across network neighborhoods of the fraction of neighbor interactions that qualify for assimilation.",
      "phenomenon": "local assimilation organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
      "source_fields": ["interaction_accepted", "network_edges"],
      "computation": {
        "op": "std",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_accepted"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "fraction"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Variability in neighborhood assimilation interaction prevalence shows how unevenly local social domains support opinion convergence."
    },
    {
      "id": "meso_neigh_rejection_std",
      "semantic_name": "Neighborhood rejection interaction variability",
      "scientific_definition": "Standard deviation across network neighborhoods of the fraction of neighbor interactions that are rejected.",
      "phenomenon": "local interaction rejection organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
      "source_fields": ["interaction_rejected", "network_edges"],
      "computation": {
        "op": "std",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_rejected"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "fraction"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Variability in neighborhood rejection interaction prevalence reveals uneven local failure of opinion change across social domains."
    },
    {
      "id": "meso_neigh_rewiring_std",
      "semantic_name": "Neighborhood adaptive rewiring variability",
      "scientific_definition": "Standard deviation across network neighborhoods of the fraction of neighbor ties successfully rewired.",
      "phenomenon": "local adaptive rewiring organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
      "source_fields": ["edge_rewired", "network_edges"],
      "computation": {
        "op": "std",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "edge_rewired"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "fraction"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Variability in neighborhood adaptive rewiring prevalence indicates how unevenly local social domains remodel their interaction ties."
    },
    {
      "id": "meso_neigh_mean_distance_std",
      "semantic_name": "Neighborhood mean interaction distance variability",
      "scientific_definition": "Standard deviation across network neighborhoods of average neighbor interaction opinion distance.",
      "phenomenon": "local interaction distance organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
      "source_fields": ["interaction_distance", "network_edges"],
      "computation": {
        "op": "std",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_distance"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Variability in neighborhood mean interaction distance captures uneven local opinion separation across social domains."
    },
    {
      "id": "meso_neigh_mean_shift_std",
      "semantic_name": "Neighborhood mean opinion update variability",
      "scientific_definition": "Standard deviation across network neighborhoods of average neighbor opinion update at each step.",
      "phenomenon": "local opinion change organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
      "source_fields": ["agent_shift", "network_edges"],
      "computation": {
        "op": "std",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "agent_shift"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Variability in neighborhood mean opinion update captures uneven local opinion change across social domains."
    },
    {
      "id": "meso_neigh_opinion_distance_corr",
      "semantic_name": "Neighborhood opinion-distance correlation",
      "scientific_definition": "Correlation across network neighborhoods between average neighbor opinion and average neighbor interaction opinion distance at each step.",
      "phenomenon": "local opinion-distance organization",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "network neighborhoods",
      "source_fields": ["state_opinion", "interaction_distance", "network_edges"],
      "computation": {
        "op": "correlation",
        "left": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "state_opinion"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "right": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_distance"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Correlation between local mean opinion and local mean interaction distance reveals whether neighborhoods with more extreme or polarized opinions also experience greater opinion separation in encounters."
    },
    {
      "id": "macro_opinion_variance",
      "semantic_name": "Whole-system opinion variance",
      "scientific_definition": "Variance of opinions across all agents before each step update.",
      "phenomenon": "global opinion heterogeneity",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole population",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "variance",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Whole-system opinion variance measures global opinion dispersion across the entire population."
    },
    {
      "id": "macro_extreme_opinion_fraction",
      "semantic_name": "Whole-system extreme opinion fraction",
      "scientific_definition": "Fraction of all agents with absolute opinion at least 0.75 at each step.",
      "phenomenon": "global polarization",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole population",
      "source_fields": ["extreme_agent_count", "agent_count"],
      "computation": {
        "op": "safe_ratio",
        "left": {"op": "field", "name": "extreme_agent_count"},
        "right": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Whole-system extreme opinion fraction tracks the global prevalence of strongly polarized opinion states."
    },
    {
      "id": "macro_network_largest_component_fraction",
      "semantic_name": "Largest network component fraction",
      "scientific_definition": "Fraction of agents contained in the largest connected component of the interaction network at each step.",
      "phenomenon": "global network integration",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole population",
      "source_fields": ["network_edges", "agent_count"],
      "computation": {
        "op": "network_largest_component_fraction",
        "edges": {"op": "field", "name": "network_edges"},
        "node_count": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Largest component fraction measures how globally connected the interaction network remains over time."
    },
    {
      "id": "macro_network_assortativity",
      "semantic_name": "Opinion assortativity of interaction network",
      "scientific_definition": "Degree of opinion similarity among connected agents in the whole interaction network at each step.",
      "phenomenon": "global opinion-network alignment",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole population",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "network_assortativity",
        "values": {"op": "field", "name": "state_opinion"},
        "edges": {"op": "field", "name": "network_edges"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Opinion assortativity indicates whether globally connected agents tend to hold similar opinions."
    }
  ],
  "interpretation_boundary": "These indicators are phase-A descriptive observables constructed only from supplied simulator semantics and raw-log fields. They do not assert causal, statistical, predictive, or intervention support. Any evidence about temporal ordering, mechanistic pathways, or intervention response is deferred to later path-generation phases after simulation statistics become available."
}
