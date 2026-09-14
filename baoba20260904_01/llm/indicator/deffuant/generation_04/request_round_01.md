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
  "indicator micro_normalized_extreme_count: Micro lacks an elementary primitive",
  "indicator meso_avg_neighborhood_opinion_mean: Meso lacks non-trivial organization",
  "indicator meso_avg_neighborhood_assimilation_fraction: Meso lacks non-trivial organization",
  "indicator meso_avg_neighborhood_backfire_fraction: Meso lacks non-trivial organization",
  "indicator meso_avg_neighborhood_rejection_fraction: Meso lacks non-trivial organization",
  "indicator meso_avg_neighborhood_rewiring_fraction: Meso lacks non-trivial organization",
  "indicator meso_avg_neighborhood_abs_shift: Meso lacks non-trivial organization",
  "indicator meso_avg_neighborhood_extreme_fraction: Meso lacks non-trivial organization",
  "interpretation_boundary must defer temporal and intervention evidence"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "deffuant",
  "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
  "indicators": [
    {
      "id": "micro_mean_opinion",
      "semantic_name": "Mean opinion across agents",
      "scientific_definition": "Time series of the average opinion state across all agents before each step update.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "assimilation_strength",
          "relationship": "direct",
          "expected_indicator_direction": "mixed",
          "rationale": "Assimilation strength affects how much opinions move toward sampled partners, but the direction of the mean depends on the full opinion configuration."
        }
      ],
      "scientific_rationale": "Tracks the central tendency of individual opinion states, a basic micro-level observable for bounded-confidence dynamics."
    },
    {
      "id": "micro_opinion_std",
      "semantic_name": "Opinion standard deviation",
      "scientific_definition": "Time series of the standard deviation of opinion states across agents before each update.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Measures the dispersion of individual opinions, reflecting the current heterogeneity of the agent population."
    },
    {
      "id": "micro_opinion_iqr",
      "semantic_name": "Opinion interquartile range",
      "scientific_definition": "Time series of the difference between the 75th and 25th percentiles of agent opinions.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "subtract",
        "left": {
          "op": "quantile",
          "input": {"op": "field", "name": "state_opinion"},
          "axis": "agent",
          "q": 0.75
        },
        "right": {
          "op": "quantile",
          "input": {"op": "field", "name": "state_opinion"},
          "axis": "agent",
          "q": 0.25
        }
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Captures the spread of the central mass of individual opinions without being dominated by extreme values."
    },
    {
      "id": "micro_extreme_opinion_fraction",
      "semantic_name": "Extreme opinion fraction",
      "scientific_definition": "Time series of the fraction of agents whose absolute opinion is at least 0.75.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "fraction",
        "input": {
          "op": "greater_equal",
          "left": {
            "op": "abs",
            "input": {"op": "field", "name": "state_opinion"}
          },
          "right": {"op": "constant", "value": 0.75}
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Tracks the prevalence of strongly polarized individual opinions, which can be influenced by repulsive and adaptive rewiring mechanisms."
    },
    {
      "id": "micro_opinion_binned_entropy",
      "semantic_name": "Binned opinion entropy",
      "scientific_definition": "Time series of binned entropy of opinion values across agents using ten bins.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "individual agents",
      "source_fields": ["state_opinion"],
      "computation": {
        "op": "binned_entropy",
        "input": {"op": "field", "name": "state_opinion"},
        "axis": "agent",
        "bins": 10
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Quantifies the diversity of the individual opinion distribution using a discretized entropy measure."
    },
    {
      "id": "micro_mean_interaction_distance",
      "semantic_name": "Mean sampled interaction distance",
      "scientific_definition": "Time series of the average absolute opinion distance across sampled interactions in each step.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_distance"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "interaction_distance"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "confidence_bound",
          "relationship": "indirect",
          "expected_indicator_direction": "unknown",
          "rationale": "Interaction distance is sampled before the acceptance test and can be influenced by the confidence bound through prior rewiring and opinion movement."
        }
      ],
      "scientific_rationale": "Summarizes the typical local opinion contrast encountered by agents in their interaction network."
    },
    {
      "id": "micro_interaction_distance_std",
      "semantic_name": "Interaction distance standard deviation",
      "scientific_definition": "Time series of the standard deviation of sampled interaction opinion distances across agents.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_distance"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "interaction_distance"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Captures variability in local opinion contrast across sampled interactions, relevant to which encounters assimilate, reject, or backfire."
    },
    {
      "id": "micro_assimilation_fraction",
      "semantic_name": "Assimilation interaction fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions where opinion distance permits assimilation.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
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
          "rationale": "A larger confidence bound permits assimilation over a wider range of opinion distances, increasing the acceptance fraction."
        }
      ],
      "scientific_rationale": "Measures the prevalence of assimilation events as a micro-level interaction process."
    },
    {
      "id": "micro_backfire_fraction",
      "semantic_name": "Backfire interaction fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions that trigger repulsive updating.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
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
          "rationale": "Raising the backfire threshold makes it harder for an interaction distance to qualify for repulsion, reducing the backfire interaction fraction."
        }
      ],
      "scientific_rationale": "Tracks the frequency of repulsive encounters as a micro-level event rate."
    },
    {
      "id": "micro_rejection_fraction",
      "semantic_name": "Rejection interaction fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions that produce neither assimilation nor repulsion.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["interaction_rejected"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "interaction_rejected"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Captures the share of rejected local encounters, which can drive adaptive network rewiring."
    },
    {
      "id": "micro_rewiring_fraction",
      "semantic_name": "Adaptive rewiring fraction",
      "scientific_definition": "Time series of the fraction of sampled interactions where the tie was successfully rewired.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "sampled pairwise interactions",
      "source_fields": ["edge_rewired"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "edge_rewired"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Measures the rate of successful tie replacement following rejected or backfire encounters."
    },
    {
      "id": "micro_mean_agent_shift",
      "semantic_name": "Mean signed opinion update",
      "scientific_definition": "Time series of the average signed opinion update applied to agents after each sampled interaction.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "per-agent elementary updates",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "mean",
        "input": {"op": "field", "name": "agent_shift"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Summarizes the average direction and magnitude of elementary opinion update events across the population."
    },
    {
      "id": "micro_mean_abs_agent_shift",
      "semantic_name": "Mean absolute opinion update",
      "scientific_definition": "Time series of the average absolute signed opinion update across agents.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "per-agent elementary updates",
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
          "rationale": "Higher assimilation strength increases the magnitude of accepted opinion updates, thereby raising the mean absolute shift."
        }
      ],
      "scientific_rationale": "Measures the typical intensity of individual opinion update events, regardless of sign."
    },
    {
      "id": "micro_agent_shift_std",
      "semantic_name": "Opinion update standard deviation",
      "scientific_definition": "Time series of the standard deviation of signed opinion updates across agents.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "per-agent elementary updates",
      "source_fields": ["agent_shift"],
      "computation": {
        "op": "std",
        "input": {"op": "field", "name": "agent_shift"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Captures heterogeneity in individual opinion update events across the agent population."
    },
    {
      "id": "micro_sign_flip_fraction",
      "semantic_name": "Sign crossing fraction",
      "scientific_definition": "Time series of the fraction of agents whose update crosses opinion zero.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "per-agent sign crossing events",
      "source_fields": ["sign_flip"],
      "computation": {
        "op": "fraction",
        "input": {"op": "field", "name": "sign_flip"},
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Tracks the occurrence of zero-crossing opinion updates as an elementary event marker of directional change."
    },
    {
      "id": "micro_normalized_extreme_count",
      "semantic_name": "Normalized extreme opinion count",
      "scientific_definition": "Time series of the supplied extreme-agent count divided by the total agent count.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "extreme-opinion agents",
      "source_fields": ["extreme_agent_count", "agent_count"],
      "computation": {
        "op": "safe_ratio",
        "left": {"op": "field", "name": "extreme_agent_count"},
        "right": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Provides a normalized prevalence measure of extreme individual opinions as a local aggregate process."
    },
    {
      "id": "meso_avg_neighborhood_opinion_mean",
      "semantic_name": "Average neighborhood mean opinion",
      "scientific_definition": "Time series of the mean across agents of each agent's local network neighborhood mean opinion.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
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
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Uses network neighborhood reduction to summarize the typical local opinion level experienced around an agent."
    },
    {
      "id": "meso_avg_neighborhood_opinion_std",
      "semantic_name": "Average neighborhood opinion variability",
      "scientific_definition": "Time series of the mean across agents of within-neighborhood opinion standard deviation.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
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
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Captures local neighborhood opinion heterogeneity, a meso-level indicator of local disagreement or clustering."
    },
    {
      "id": "meso_avg_neighborhood_assimilation_fraction",
      "semantic_name": "Average neighborhood assimilation fraction",
      "scientific_definition": "Time series of the mean across agents of the fraction of assimilation interactions within each local neighborhood.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
      "source_fields": ["interaction_accepted", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_accepted"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "fraction"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "confidence_bound",
          "relationship": "indirect",
          "expected_indicator_direction": "increase",
          "rationale": "A larger confidence bound increases assimilation events locally, raising the average neighborhood assimilation fraction."
        }
      ],
      "scientific_rationale": "Measures the local prevalence of assimilative interactions using network-based neighborhood reduction."
    },
    {
      "id": "meso_avg_neighborhood_backfire_fraction",
      "semantic_name": "Average neighborhood backfire fraction",
      "scientific_definition": "Time series of the mean across agents of the fraction of backfire interactions within each local neighborhood.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
      "source_fields": ["interaction_backfire", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {"op": "field", "name": "interaction_backfire"},
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "fraction"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "backfire_threshold",
          "relationship": "indirect",
          "expected_indicator_direction": "decrease",
          "rationale": "Raising the backfire threshold reduces local backfire eligibility, lowering neighborhood backfire shares."
        }
      ],
      "scientific_rationale": "Captures the local prevalence of repulsive interactions via explicit network neighborhood reduction."
    },
    {
      "id": "meso_avg_neighborhood_rejection_fraction",
      "semantic_name": "Average neighborhood rejection fraction",
      "scientific_definition": "Time series of the mean across agents of the fraction of rejected interactions within each local neighborhood.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
      "source_fields": ["interaction_rejected", "network_edges"],
      "computation": {
        "op": "mean",
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
      "scientific_rationale": "Measures local prevalence of neither-assimilation nor repulsion encounters, which can trigger adaptive rewiring."
    },
    {
      "id": "meso_avg_neighborhood_rewiring_fraction",
      "semantic_name": "Average neighborhood rewiring fraction",
      "scientific_definition": "Time series of the mean across agents of the fraction of rewired ties within each local neighborhood.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
      "source_fields": ["edge_rewired", "network_edges"],
      "computation": {
        "op": "mean",
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
      "scientific_rationale": "Tracks local rewiring activity through network neighborhood reduction, indicating adaptive topological change at the meso scale."
    },
    {
      "id": "meso_avg_neighborhood_abs_shift",
      "semantic_name": "Average neighborhood mean absolute update",
      "scientific_definition": "Time series of the mean across agents of local neighborhood mean absolute opinion update.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
      "source_fields": ["agent_shift", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "abs",
            "input": {"op": "field", "name": "agent_shift"}
          },
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "mean"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [
        {
          "parameter": "assimilation_strength",
          "relationship": "indirect",
          "expected_indicator_direction": "increase",
          "rationale": "Higher assimilation strength increases update magnitudes, thereby raising mean absolute shifts inside local neighborhoods."
        }
      ],
      "scientific_rationale": "Captures local intensity of opinion update events through a network neighborhood reduction operation."
    },
    {
      "id": "meso_avg_neighborhood_extreme_fraction",
      "semantic_name": "Average neighborhood extreme opinion fraction",
      "scientific_definition": "Time series of the mean across agents of the fraction of extreme opinions inside each local neighborhood.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "meso",
      "entity_scope": "neighborhood",
      "entities": "local network neighborhoods",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "mean",
        "input": {
          "op": "network_neighborhood_reduce",
          "values": {
            "op": "greater_equal",
            "left": {
              "op": "abs",
              "input": {"op": "field", "name": "state_opinion"}
            },
            "right": {"op": "constant", "value": 0.75}
          },
          "edges": {"op": "field", "name": "network_edges"},
          "reducer": "fraction"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Uses network neighborhood reduction to measure local polarization in opinion values at the meso scale."
    },
    {
      "id": "macro_network_density",
      "semantic_name": "Global network density",
      "scientific_definition": "Time series of the density of the undirected interaction network at the start of each step.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole interaction network",
      "source_fields": ["network_edges", "agent_count"],
      "computation": {
        "op": "network_density",
        "edges": {"op": "field", "name": "network_edges"},
        "node_count": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Provides a whole-system topological summary of the interaction network, useful for tracking global structural change."
    },
    {
      "id": "macro_largest_component_fraction",
      "semantic_name": "Largest network component fraction",
      "scientific_definition": "Time series of the fraction of agents in the largest connected component of the interaction network.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole interaction network",
      "source_fields": ["network_edges", "agent_count"],
      "computation": {
        "op": "network_largest_component_fraction",
        "edges": {"op": "field", "name": "network_edges"},
        "node_count": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Measures global connectivity by the size of the dominant connected component, a macro-level network outcome."
    },
    {
      "id": "macro_network_component_count",
      "semantic_name": "Connected component count",
      "scientific_definition": "Time series of the number of connected components in the interaction network.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole interaction network",
      "source_fields": ["network_edges", "agent_count"],
      "computation": {
        "op": "network_component_count",
        "edges": {"op": "field", "name": "network_edges"},
        "node_count": {"op": "field", "name": "agent_count"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Tracks whole-system fragmentation or integration through the number of connected components in the adaptive network."
    },
    {
      "id": "macro_network_assortativity",
      "semantic_name": "Opinion-based network assortativity",
      "scientific_definition": "Time series of network assortativity with respect to agent opinion values on the current interaction network.",
      "phenomenon": "Opinion assimilation and adaptive network rewiring under bounded confidence",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole interaction network",
      "source_fields": ["state_opinion", "network_edges"],
      "computation": {
        "op": "network_assortativity",
        "values": {"op": "field", "name": "state_opinion"},
        "edges": {"op": "field", "name": "network_edges"}
      },
      "temporal_aggregation": {"op": "identity", "window": null},
      "parameter_associations": [],
      "scientific_rationale": "Quantifies global opinion-tie correlation in the interaction network, a collective structure-attribute relationship."
    }
  ],
  "interpretation_boundary": "Indicators are descriptive observables only; no causal, statistical, or predictive claims are made. Scale follows the scientific entity contract and is not a time-window label."
}
