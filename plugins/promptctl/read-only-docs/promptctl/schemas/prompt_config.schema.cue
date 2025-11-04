package promptctl

// promptctl configuration schema
#Config: {
	prompts: [...#PromptEntry] & [_, ...] // at least one item required
}

// A prompt entry can be either a simple string or an advanced prompt node
#PromptEntry: #StringPrompt | #PromptNode

// String form must have at least 1 character
#StringPrompt: string & =~"^.+"

// Base prompt node with required kind field
#PromptNode: {
	kind: "prompt" | "template" | "chain" | "map" | "reduce" | "when"
	...
} & (#PromptLeaf | #TemplateNode | #ChainNode | #MapNode | #ReduceNode | #WhenNode)

// Leaf prompt node for direct LLM calls
#PromptLeaf: {
	kind:        "prompt"
	name?:       string
	model?:      string
	system?:     string
	user?:       string
	max_tokens?: int & >=1
	temperature?: number & >=0
}

// Template node for string interpolation
#TemplateNode: {
	kind:     "template"
	name?:    string
	input?:   {...} // arbitrary object
	template: string & =~"^.+" // at least 1 character
}

// Chain node for sequential execution
#ChainNode: {
	kind:  "chain"
	name?: string
	steps: [...#PromptNode] & [_, ...] // at least one step required
}

// Map node for parallel execution over a dataset
#MapNode: {
	kind:         "map"
	over:         string & =~"^.+" // e.g., a glob or dataset handle
	step:         #PromptNode
	concurrency?: int & >=1
}

// Reduce node for aggregating multiple inputs
#ReduceNode: {
	kind:    "reduce"
	inputs:  [...#PromptNode] & [_, ...] // at least one input required
	reducer: #PromptNode
}

// When node for conditional execution
#WhenNode: {
	kind: "when"
	if:   string & =~"^.+" // boolean expression string, evaluated by promptctl
	then: #PromptNode
	else?: #PromptNode
}