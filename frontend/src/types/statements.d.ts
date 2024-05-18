export interface Statement {
    area: String,
    company: Number,
    description: String,
    id: number,
    level: String,
    name: String,
    question: String,
    severity: String,
    status: String,
    title: String,
    type: String,
}

export interface Statements extends Array<Statement> {}