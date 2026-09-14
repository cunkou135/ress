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
  "indicator meso_district_local_similarity_entropy: entropy accepts only categorical, boolean, or integer-like input; use binned_entropy for continuous values",
  "indicator meso_district_unhappy_fraction_entropy: entropy accepts only categorical, boolean, or integer-like input; use binned_entropy for continuous values"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "schelling",
  "phenomenon": "Schelling segregation dynamics",
  "indicators": [
    {
      "id": "micro_local_similarity_mean",
      "semantic_name": "Mean local same-group similarity",
      "scientific_definition": "Average same-group fraction among occupied Moore neighbours across all agents at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "direct",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance changes the satisfaction threshold that triggers moves, so average local similarity may shift through relocation flows."
        }
      ],
      "scientific_rationale": "This time series tracks average local group exposure, a basic primitive of the Schelling relocation rule."
    },
    {
      "id": "micro_local_similarity_std",
      "semantic_name": "Dispersion of local same-group similarity",
      "scientific_definition": "Standard deviation across agents of local same-group similarity at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "A time series of individual local similarity dispersion reveals how homogeneous agent exposures are across the population."
    },
    {
      "id": "micro_local_similarity_median",
      "semantic_name": "Median local same-group similarity",
      "scientific_definition": "Median same-group fraction among occupied Moore neighbours across all agents at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
        "q": 0.5
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "The median local similarity gives a robust central tendency for individual local exposure without assuming interval averages."
    },
    {
      "id": "micro_local_similarity_quantile_90",
      "semantic_name": "90th percentile local same-group similarity",
      "scientific_definition": "90th percentile of agent-level local same-group similarity at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
        "q": 0.9
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "High quantile local similarity tracks the upper tail of individual local group exposure across the population."
    },
    {
      "id": "micro_unhappy_fraction",
      "semantic_name": "Unsatisfied agent fraction",
      "scientific_definition": "Share of agents whose local same-group fraction is below tolerance at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "A higher tolerance makes more agents classify as unsatisfied at the same local similarity, increasing the unsatisfied fraction."
        }
      ],
      "scientific_rationale": "This observable tracks prevalence of the elementary dissatisfaction event that drives relocation in the model."
    },
    {
      "id": "micro_moved_fraction",
      "semantic_name": "Moved agent fraction",
      "scientific_definition": "Share of agents that relocated during each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move probability increases the chance that unsatisfied agents attempt relocation, so the moved fraction rises."
        }
      ],
      "scientific_rationale": "Moved fraction is a direct elementary event observable for relocation activity in the model."
    },
    {
      "id": "micro_boundary_fraction",
      "semantic_name": "Boundary-exposed agent fraction",
      "scientific_definition": "Share of agents with at least one occupied different-group neighbour at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "direct",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance affects relocation which can alter the number of agents exposed to different-group neighbours."
        }
      ],
      "scientific_rationale": "Boundary exposure is a local interaction primitive capturing contact between groups."
    },
    {
      "id": "micro_mean_move_distance",
      "semantic_name": "Mean relocation distance",
      "scientific_definition": "Average periodic Manhattan distance moved by agents during each recorded step, with zeros for non-movers.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "agents",
      "source_fields": [
        "move_distance"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "field",
          "name": "move_distance"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "direct",
          "expected_indicator_direction": "mixed",
          "rationale": "Move probability affects how many agents move but not directly the distances they choose; the mean distance may change indirectly."
        }
      ],
      "scientific_rationale": "This time series summarizes the microscopic relocation distance primitive across all agents."
    },
    {
      "id": "micro_move_distance_std",
      "semantic_name": "Dispersion of relocation distance",
      "scientific_definition": "Standard deviation across agents of periodic Manhattan relocation distance at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "Dispersion of relocation distance captures variability in the extent of individual moves."
    },
    {
      "id": "micro_destination_similarity_mean",
      "semantic_name": "Mean destination similarity",
      "scientific_definition": "Average same-group neighbour fraction at selected destinations across all agents, with zeros for non-movers.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agents",
      "source_fields": [
        "destination_similarity"
      ],
      "computation": {
        "op": "mean",
        "input": {
          "op": "field",
          "name": "destination_similarity"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher destination preference biases movers toward the most similar sampled vacancy, increasing selected destination similarity."
        }
      ],
      "scientific_rationale": "This observable tracks the local exposure obtained through destination selection, a key relocation interaction."
    },
    {
      "id": "micro_destination_similarity_std",
      "semantic_name": "Dispersion of destination similarity",
      "scientific_definition": "Standard deviation across agents of same-group neighbour fraction at selected destinations, with zeros for non-movers.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "relationship": "direct",
          "expected_indicator_direction": "mixed",
          "rationale": "Higher destination preference can concentrate destination similarity values, changing their spread, but the direction depends on sampled vacancies."
        }
      ],
      "scientific_rationale": "Dispersion of destination exposure reveals how variable relocation outcomes are across agents."
    },
    {
      "id": "micro_neighbour_count_mean",
      "semantic_name": "Mean occupied neighbour count",
      "scientific_definition": "Average number of occupied Moore neighbours per agent at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "Local occupancy is a local primitive that conditions neighbour similarity and satisfaction."
    },
    {
      "id": "micro_neighbour_count_std",
      "semantic_name": "Dispersion of occupied neighbour count",
      "scientific_definition": "Standard deviation across agents of occupied Moore-neighbour count at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "Dispersion of local occupancy indicates heterogeneity in the crowdedness of agent neighbourhoods."
    },
    {
      "id": "micro_local_similarity_binned_entropy",
      "semantic_name": "Entropy of binned local similarity",
      "scientific_definition": "Binned entropy of agent-level local same-group similarity at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "Binned entropy captures distributional complexity of individual local similarity across the population."
    },
    {
      "id": "micro_local_similarity_quantile_10",
      "semantic_name": "10th percentile local same-group similarity",
      "scientific_definition": "10th percentile of agent-level local same-group similarity at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents",
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
        "q": 0.1
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "The lower tail of local similarity identifies how many agents reside in highly heterogeneous local environments."
    },
    {
      "id": "micro_local_similarity_move_distance_correlation",
      "semantic_name": "Correlation between local similarity and move distance",
      "scientific_definition": "Cross-agent correlation between local same-group similarity and relocation distance at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agents",
      "source_fields": [
        "local_similarity",
        "move_distance"
      ],
      "computation": {
        "op": "correlation",
        "left": {
          "op": "field",
          "name": "local_similarity"
        },
        "right": {
          "op": "field",
          "name": "move_distance"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "direct",
          "expected_indicator_direction": "mixed",
          "rationale": "Move probability controls the volume of relocation, changing which pairs of local similarity and distance are observed."
        }
      ],
      "scientific_rationale": "This interaction observable relates local dissatisfaction context to relocation distance at the agent level."
    },
    {
      "id": "meso_district_local_similarity_std",
      "semantic_name": "Between-district dispersion of local similarity",
      "scientific_definition": "Standard deviation across fixed spatial districts of district-level mean local same-group similarity at each step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "local_similarity"
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance changes relocation pressure and may affect how district mean similarities diverge or converge."
        }
      ],
      "scientific_rationale": "This observable captures whether local group exposure becomes more uneven across real public districts over time."
    },
    {
      "id": "meso_district_unhappy_fraction_std",
      "semantic_name": "Between-district dispersion of unsatisfied fraction",
      "scientific_definition": "Standard deviation across fixed spatial districts of district-level unsatisfied agent fraction at each step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "unhappy"
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance directly changes individual dissatisfaction, but district-level averages also depend on relocation and sorting."
        }
      ],
      "scientific_rationale": "Measures whether dissatisfaction is distributed unevenly across public spatial districts."
    },
    {
      "id": "meso_district_boundary_fraction_std",
      "semantic_name": "Between-district dispersion of boundary exposure",
      "scientific_definition": "Standard deviation across fixed spatial districts of district-level fraction of agents with at least one different-group neighbour.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "boundary_agent"
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance affects relocation and therefore the amount of different-group contact within districts."
        }
      ],
      "scientific_rationale": "District-level boundary exposure dispersion summarizes spatial inequality in local intergroup contact across public subdomains."
    },
    {
      "id": "meso_district_move_distance_std",
      "semantic_name": "Between-district dispersion of relocation distance",
      "scientific_definition": "Standard deviation across fixed spatial districts of district-level mean relocation distance at each step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "move_distance"
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Move probability changes relocation volume which can alter district-level average distances."
        }
      ],
      "scientific_rationale": "Captures whether relocation distances become more unequal across public spatial districts."
    },
    {
      "id": "meso_district_destination_similarity_std",
      "semantic_name": "Between-district dispersion of destination similarity",
      "scientific_definition": "Standard deviation across fixed spatial districts of district-level mean destination same-group similarity at each step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "destination_similarity"
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Destination preference affects where agents move within or between districts and thus district destination similarity."
        }
      ],
      "scientific_rationale": "Measures whether district-level destination exposure becomes more spatially uneven over time."
    },
    {
      "id": "meso_district_neighbour_count_std",
      "semantic_name": "Between-district dispersion of occupied neighbour count",
      "scientific_definition": "Standard deviation across fixed spatial districts of district-level mean occupied Moore-neighbour count at each step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "neighbour_count"
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [],
      "scientific_rationale": "Summarizes how much local occupancy varies across real public spatial districts."
    },
    {
      "id": "meso_district_local_similarity_entropy",
      "semantic_name": "Entropy of district mean local similarity",
      "scientific_definition": "Entropy across fixed spatial districts of district-level mean local same-group similarity at each step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "local_similarity"
      ],
      "computation": {
        "op": "entropy",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance changes relocation choices and may alter the distribution of district mean similarities."
        }
      ],
      "scientific_rationale": "Entropy over district-level averages reveals how concentrated or dispersed local similarity is across the district system."
    },
    {
      "id": "meso_district_unhappy_fraction_entropy",
      "semantic_name": "Entropy of district unsatisfied fraction",
      "scientific_definition": "Entropy across fixed spatial districts of district-level unsatisfied agent fraction at each step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts",
      "source_fields": [
        "district_id",
        "unhappy"
      ],
      "computation": {
        "op": "entropy",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance changes dissatisfaction thresholds and may alter how those fractions are distributed across districts."
        }
      ],
      "scientific_rationale": "Entropy of district dissatisfaction prevalence reveals whether dissatisfaction is spread broadly or concentrated in certain public districts."
    },
    {
      "id": "macro_global_unhappy_count",
      "semantic_name": "Total unsatisfied agents",
      "scientific_definition": "Number of unsatisfied agents in the whole system at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole system",
      "source_fields": [
        "unhappy_count"
      ],
      "computation": {
        "op": "field",
        "name": "unhappy_count"
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher tolerance increases the number of agents classified as unsatisfied from identical local conditions."
        }
      ],
      "scientific_rationale": "This whole-system aggregate tracks the total volume of dissatisfaction across the entire grid."
    },
    {
      "id": "macro_global_move_count",
      "semantic_name": "Total moves",
      "scientific_definition": "Total number of agent relocations in the whole system during each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole system",
      "source_fields": [
        "moved",
        "agent_count"
      ],
      "computation": {
        "op": "multiply",
        "left": {
          "op": "fraction",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "relationship": "direct",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move probability increases relocation attempts among unsatisfied agents, increasing total system-wide moves."
        }
      ],
      "scientific_rationale": "Total moves is a whole-system relocation outcome derived from the fraction of moved agents and the system population size."
    },
    {
      "id": "macro_spatial_neighbor_similarity",
      "semantic_name": "Global spatial neighbor similarity",
      "scientific_definition": "Whole-system spatial neighbour similarity computed from the periodic occupancy grid at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole system grid",
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
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Destination preference alters where agents move, which can reshape global neighbor similarity without a fixed sign."
        }
      ],
      "scientific_rationale": "This global structural observable measures whole-system spatial sorting directly from the occupancy grid."
    },
    {
      "id": "macro_largest_component_fraction",
      "semantic_name": "Largest same-group component fraction",
      "scientific_definition": "Fraction of the grid occupied by the largest connected component of same-group occupied cells at each recorded step.",
      "phenomenon": "Schelling segregation dynamics",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "whole system grid",
      "source_fields": [
        "state_grid"
      ],
      "computation": {
        "op": "largest_component_fraction",
        "input": {
          "op": "field",
          "name": "state_grid"
        }
      },
      "temporal_aggregation": {
        "op": "identity",
        "window": null
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "relationship": "indirect",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance changes relocation pressure and may alter the size of dominant same-group connected components at the whole-system scale."
        }
      ],
      "scientific_rationale": "Largest component fraction is a global structural statistic for whole-system spatial clustering."
    }
  ],
  "interpretation_boundary": "These indicators are descriptive, executable observables only. They do not establish temporal precedence, statistical association, causal effects, or intervention outcomes. District-level indicators use the fixed public spatial district primitive and do not infer segregation outcomes or represent causal pathways."
}
