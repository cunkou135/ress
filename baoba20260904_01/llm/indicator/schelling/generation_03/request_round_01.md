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
  "indicator micro_unsatisfied_agent_count: sum requires numeric input",
  "indicator micro_fraction_unsatisfied: sum requires numeric input",
  "indicator micro_sum_relocation_count: sum requires numeric input",
  "indicator micro_count_boundary_agents: sum requires numeric input",
  "indicator meso_district_mean_local_similarity: Meso lacks non-trivial organization",
  "indicator meso_district_unhappy_fraction_mean: Meso lacks non-trivial organization",
  "indicator meso_district_boundary_fraction_mean: Meso lacks non-trivial organization",
  "indicator meso_district_move_fraction_mean: Meso lacks non-trivial organization",
  "indicator meso_district_destination_similarity_mean: Meso lacks non-trivial organization",
  "indicator meso_district_group_composition_entropy: entropy accepts only categorical, boolean, or integer-like input; use binned_entropy for continuous values",
  "interpretation_boundary must defer temporal and intervention evidence"
]
Return a complete corrected object without using simulation outcomes.
{
  "scenario": "schelling",
  "phenomenon": "Schelling segregation",
  "indicators": [
    {
      "id": "micro_unsatisfied_agent_count",
      "semantic_name": "Count of unsatisfied agents",
      "scientific_definition": "Number of agents whose occupied-neighbour same-group fraction is below tolerance in the current recorded step.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "agents with unhappy boolean",
      "source_fields": [
        "unhappy"
      ],
      "computation": {
        "op": "sum",
        "input": {
          "op": "field",
          "name": "unhappy"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "expected_indicator_direction": "decrease",
          "rationale": "Higher tolerance lowers the required similarity for satisfaction, so fewer agents are classified as unhappy at equal local similarity."
        }
      ],
      "scientific_rationale": "Unhappy events are elementary dissatisfaction signals; counting them measures the prevalence of local dissatisfaction over time."
    },
    {
      "id": "micro_fraction_unsatisfied",
      "semantic_name": "Fraction of unsatisfied agents",
      "scientific_definition": "Proportion of all agents classified as unhappy in the current step.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "unhappy agents and population",
      "source_fields": [
        "unhappy",
        "agent_count"
      ],
      "computation": {
        "op": "safe_ratio",
        "left": {
          "op": "sum",
          "input": {
            "op": "field",
            "name": "unhappy"
          },
          "axis": "agent"
        },
        "right": {
          "op": "field",
          "name": "agent_count"
        }
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "expected_indicator_direction": "decrease",
          "rationale": "A higher tolerance threshold makes more agents satisfied, reducing the unsatisfied proportion."
        }
      ],
      "scientific_rationale": "This indicator normalizes the count of elementary dissatisfaction events by population size, allowing comparisons across parameter settings."
    },
    {
      "id": "micro_mean_local_similarity",
      "semantic_name": "Mean local same-group similarity",
      "scientific_definition": "Average same-group fraction among occupied Moore neighbours across agents.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents with local similarity",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "expected_indicator_direction": "increase",
          "rationale": "Stronger destination preference selects sampled vacancies with higher local similarity, raising the average local similarity after relocations."
        }
      ],
      "scientific_rationale": "Mean local similarity summarizes individual exposure to same-group neighbours, a core micro-level driver of satisfaction."
    },
    {
      "id": "micro_std_local_similarity",
      "semantic_name": "Dispersion of local similarities",
      "scientific_definition": "Standard deviation of same-group fraction among occupied Moore neighbours across agents.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents with local similarity",
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
        "op": "identity"
      },
      "scientific_rationale": "Dispersion across individual local similarities captures heterogeneity in agents' local social environments."
    },
    {
      "id": "micro_median_local_similarity",
      "semantic_name": "Median local same-group similarity",
      "scientific_definition": "Median same-group fraction among occupied Moore neighbours across agents.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "agents with local similarity",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "expected_indicator_direction": "increase",
          "rationale": "When destination preference is high, relocation targets are more similar, likely shifting the median exposure upward."
        }
      ],
      "scientific_rationale": "The median provides a robust central measure of individual local exposure that is less sensitive to extreme local similarities."
    },
    {
      "id": "micro_entropy_local_similarity",
      "semantic_name": "Binned entropy of local similarities",
      "scientific_definition": "Binned entropy of the distribution of agent-level local same-group similarities.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "individual",
      "entities": "distribution of local_similarity values",
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
        "op": "identity"
      },
      "scientific_rationale": "Entropy of binned local similarities measures diversity of individual local environments, indicating how mixed or sorted agents' exposures are."
    },
    {
      "id": "micro_mean_neighbour_count",
      "semantic_name": "Mean occupied neighbour count",
      "scientific_definition": "Average number of occupied Moore neighbours across agents.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents with occupied neighbour count",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "expected_indicator_direction": "mixed",
          "rationale": "Tolerance changes which agents are unsatisfied and may alter relocation patterns, but its effect on occupied neighbour count is not monotonic."
        }
      ],
      "scientific_rationale": "Local occupancy affects the denominator of similarity, shaping the information available to individuals when they evaluate satisfaction."
    },
    {
      "id": "micro_std_neighbour_count",
      "semantic_name": "Dispersion of occupied neighbour counts",
      "scientific_definition": "Standard deviation of occupied Moore-neighbour counts across agents.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "local_process",
      "entities": "agents with occupied neighbour count",
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
        "op": "identity"
      },
      "scientific_rationale": "Variation in local occupancy reflects the unevenness of crowding or vacancy distribution in agents' local neighbourhoods."
    },
    {
      "id": "micro_fraction_boundary_agents",
      "semantic_name": "Fraction of boundary agents",
      "scientific_definition": "Proportion of agents that have at least one occupied different-group neighbour.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agents with boundary exposure",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "expected_indicator_direction": "decrease",
          "rationale": "Higher destination preference selects more similar destination neighbourhoods, reducing contact with different-group neighbours."
        }
      ],
      "scientific_rationale": "Boundary agents mark local inter-group contacts; a decreasing fraction indicates stronger spatial separation."
    },
    {
      "id": "micro_mean_move_distance",
      "semantic_name": "Mean relocation distance",
      "scientific_definition": "Average periodic Manhattan distance of relocations across all agents, with non-movers contributing zero.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "relocation events with distance",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move probability increases the number of attempted relocations, making more agents move and raising the average recorded relocation distance."
        }
      ],
      "scientific_rationale": "Mean relocation distance reflects how far agents move when they choose or are able to relocate."
    },
    {
      "id": "micro_fraction_relocated",
      "semantic_name": "Fraction of relocated agents",
      "scientific_definition": "Proportion of agents that relocated during the current step.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "agents with moved flag",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move probability means unsatisfied agents are more likely to relocate in a given step, increasing the fraction moved."
        }
      ],
      "scientific_rationale": "This indicator captures the aggregate activity of elementary relocation events at the micro level."
    },
    {
      "id": "micro_sum_relocation_count",
      "semantic_name": "Total relocation events",
      "scientific_definition": "Number of agents that relocated during the current step.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "agents with moved flag",
      "source_fields": [
        "moved"
      ],
      "computation": {
        "op": "sum",
        "input": {
          "op": "field",
          "name": "moved"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "move_probability",
          "expected_indicator_direction": "increase",
          "rationale": "Higher move probability increases the frequency of relocation attempts, leading to more recorded moved events."
        }
      ],
      "scientific_rationale": "Total relocation events measure the absolute level of micro-level mobility in the system."
    },
    {
      "id": "micro_mean_destination_similarity",
      "semantic_name": "Mean destination similarity",
      "scientific_definition": "Average same-group neighbour fraction at selected destinations across all agents, with non-movers contributing zero.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "elementary_event",
      "entities": "destination similarity values",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "expected_indicator_direction": "increase",
          "rationale": "Higher destination preference directly selects the sampled vacancy with the highest local similarity, increasing destination similarity."
        }
      ],
      "scientific_rationale": "Destination similarity is a direct trace of the relocation choice mechanism, making it sensitive to destination_preference."
    },
    {
      "id": "micro_correlation_similarity_neighbour_count",
      "semantic_name": "Agent-level correlation between local similarity and neighbour count",
      "scientific_definition": "Correlation across agents between local same-group similarity and occupied neighbour count.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agent local similarity and neighbour count",
      "source_fields": [
        "local_similarity",
        "neighbour_count"
      ],
      "computation": {
        "op": "correlation",
        "left": {
          "op": "field",
          "name": "local_similarity"
        },
        "right": {
          "op": "field",
          "name": "neighbour_count"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "scientific_rationale": "This interaction-level indicator reveals how individual local similarity covaries with the amount of local occupancy."
    },
    {
      "id": "micro_correlation_similarity_move_distance",
      "semantic_name": "Agent-level correlation between local similarity and move distance",
      "scientific_definition": "Correlation across agents between local same-group similarity and relocation distance.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agent local similarity and move distance",
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
        "op": "identity"
      },
      "scientific_rationale": "This interaction-level indicator captures whether agents with lower local similarity tend to move farther when relocating."
    },
    {
      "id": "micro_count_boundary_agents",
      "semantic_name": "Count of boundary agents",
      "scientific_definition": "Number of agents with at least one occupied different-group neighbour.",
      "phenomenon": "Schelling segregation",
      "scale": "micro",
      "entity_scope": "interaction",
      "entities": "agents with boundary exposure",
      "source_fields": [
        "boundary_agent"
      ],
      "computation": {
        "op": "sum",
        "input": {
          "op": "field",
          "name": "boundary_agent"
        },
        "axis": "agent"
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "expected_indicator_direction": "decrease",
          "rationale": "Higher destination preference promotes sorting into homogeneous neighbourhoods, reducing the number of agents exposed to different-group neighbours."
        }
      ],
      "scientific_rationale": "Counting boundary agents provides an absolute micro-level measure of inter-group contact across the population."
    },
    {
      "id": "meso_district_mean_local_similarity",
      "semantic_name": "Mean district-level local similarity",
      "scientific_definition": "Average across spatial districts of the mean local same-group similarity within each district.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
      "source_fields": [
        "local_similarity",
        "district_id"
      ],
      "computation": {
        "op": "mean",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "expected_indicator_direction": "increase",
          "rationale": "Higher destination preference can raise district-level local similarity by encouraging homophilic relocation within spatial domains."
        }
      ],
      "scientific_rationale": "Districts are real spatial domains; this indicator summarizes the typical district-level local exposure using group_reduce over district membership."
    },
    {
      "id": "meso_district_std_local_similarity",
      "semantic_name": "Mean district dispersion of local similarity",
      "scientific_definition": "Average across spatial districts of the within-district standard deviation of local same-group similarity.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
      "source_fields": [
        "local_similarity",
        "district_id"
      ],
      "computation": {
        "op": "mean",
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
          "reducer": "std"
        },
        "axis": "group"
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "scientific_rationale": "This meso indicator captures the typical heterogeneity of individual similarity within spatial districts, reflecting district-level mixing."
    },
    {
      "id": "meso_district_unhappy_fraction_mean",
      "semantic_name": "Mean district unhappy fraction",
      "scientific_definition": "Average across spatial districts of the fraction of unsatisfied agents within each district.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
      "source_fields": [
        "unhappy",
        "district_id"
      ],
      "computation": {
        "op": "mean",
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
        "op": "identity"
      },
      "scientific_rationale": "Districts organize local dissatisfaction; averaging the unhappy fraction across districts gives a meso-level summary of dissatisfied spatial domains."
    },
    {
      "id": "meso_district_unhappy_fraction_std",
      "semantic_name": "Between-district variation in unhappy fraction",
      "scientific_definition": "Standard deviation across spatial districts of the district-level unsatisfied fraction.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
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
      "temporal_aggregation": {
        "op": "identity"
      },
      "scientific_rationale": "Variation in unhappy fraction across districts indicates whether dissatisfaction is spatially concentrated or spread evenly across local domains."
    },
    {
      "id": "meso_district_boundary_fraction_mean",
      "semantic_name": "Mean district boundary-agent fraction",
      "scientific_definition": "Average across spatial districts of the proportion of agents with at least one occupied different-group neighbour.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
      "source_fields": [
        "boundary_agent",
        "district_id"
      ],
      "computation": {
        "op": "mean",
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
        "op": "identity"
      },
      "scientific_rationale": "Boundary-agent fractions measured per district capture the typical amount of inter-group contact within real spatial domains."
    },
    {
      "id": "meso_district_move_fraction_mean",
      "semantic_name": "Mean district relocation fraction",
      "scientific_definition": "Average across spatial districts of the proportion of agents that relocated during the current step.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
      "source_fields": [
        "moved",
        "district_id"
      ],
      "computation": {
        "op": "mean",
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
      "temporal_aggregation": {
        "op": "identity"
      },
      "scientific_rationale": "District-level relocation activity reveals which spatial domains experience the most mobility, aggregated to a typical district value."
    },
    {
      "id": "meso_district_destination_similarity_mean",
      "semantic_name": "Mean district destination similarity",
      "scientific_definition": "Average across spatial districts of the mean destination similarity of agents originating in each district.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
      "source_fields": [
        "destination_similarity",
        "district_id"
      ],
      "computation": {
        "op": "mean",
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
        "op": "identity"
      },
      "scientific_rationale": "Destination choices vary across districts; this meso indicator summarizes the typical quality of destinations selected by residents of each spatial domain."
    },
    {
      "id": "meso_district_group_composition_entropy",
      "semantic_name": "Spatial entropy of district group composition",
      "scientific_definition": "Entropy across spatial districts of the proportion of group-1 agents in each district.",
      "phenomenon": "Schelling segregation",
      "scale": "meso",
      "entity_scope": "district",
      "entities": "spatial districts with resident agents",
      "source_fields": [
        "agent_group",
        "district_id"
      ],
      "computation": {
        "op": "entropy",
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
          "reducer": "mean"
        },
        "axis": "group"
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "scientific_rationale": "District-level group composition quantifies spatial segregation; higher entropy means district compositions are more mixed, while lower entropy indicates homogeneous spatial domains."
    },
    {
      "id": "macro_global_neighbor_similarity",
      "semantic_name": "Global spatial neighbor similarity",
      "scientific_definition": "Whole-grid average of same-group similarity between occupied Moore neighbours computed directly from the spatial configuration.",
      "phenomenon": "Schelling segregation",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "occupied periodic grid cells",
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
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "destination_preference",
          "expected_indicator_direction": "increase",
          "rationale": "Stronger homophilic relocation increases global spatial sorting, raising whole-grid neighbour similarity."
        }
      ],
      "scientific_rationale": "This global structure measure directly quantifies the degree of same-group adjacency across the entire periodic grid."
    },
    {
      "id": "macro_global_largest_component_fraction",
      "semantic_name": "Largest occupied component fraction",
      "scientific_definition": "Fraction of occupied grid cells contained in the largest connected occupied component of the periodic grid.",
      "phenomenon": "Schelling segregation",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "occupied periodic grid cells",
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
        "op": "identity"
      },
      "scientific_rationale": "A large connected occupied component fraction indicates that most cells are part of a giant spatial cluster, a macro-level structural outcome."
    },
    {
      "id": "macro_global_connected_component_count",
      "semantic_name": "Connected occupied component count",
      "scientific_definition": "Number of connected occupied components in the periodic grid.",
      "phenomenon": "Schelling segregation",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "occupied periodic grid cells",
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
      "temporal_aggregation": {
        "op": "identity"
      },
      "scientific_rationale": "The number of connected occupied components is a global structural property reflecting spatial fragmentation across the entire system."
    },
    {
      "id": "macro_global_dissatisfaction_fraction",
      "semantic_name": "Whole-system dissatisfaction fraction",
      "scientific_definition": "Total unsatisfied agents divided by the number of agents in the simulation.",
      "phenomenon": "Schelling segregation",
      "scale": "macro",
      "entity_scope": "whole_system",
      "entities": "all agents",
      "source_fields": [
        "unhappy_count",
        "agent_count"
      ],
      "computation": {
        "op": "safe_ratio",
        "left": {
          "op": "field",
          "name": "unhappy_count"
        },
        "right": {
          "op": "field",
          "name": "agent_count"
        }
      },
      "temporal_aggregation": {
        "op": "identity"
      },
      "parameter_associations": [
        {
          "parameter": "tolerance",
          "expected_indicator_direction": "decrease",
          "rationale": "Higher tolerance makes agents satisfied at lower similarity levels, reducing the whole-system dissatisfaction fraction."
        }
      ],
      "scientific_rationale": "This macro indicator aggregates all individual dissatisfaction events into a single whole-system prevalence measure at each step."
    }
  ],
  "interpretation_boundary": "Indicators are descriptive only and are generated from the supplied raw log schema and grammar. They do not establish causal, statistical, or intervention claims, and no candidate paths, edges, or predictions are implied at this phase."
}
