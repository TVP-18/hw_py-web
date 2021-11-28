AD_CREATE = {
	"type": "object",
	"properties": {
		"title": {
			"type": "string"
		},
		"text": {
			"type": "string"
		},
		"id_owner": {
			"type": "number",
			"minimum": 1
		},
	},
	"required": ["title", "text", "id_owner"]
}
