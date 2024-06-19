export interface Statement {
    area: String,
    company: Number,
    description: String,
    id: number,
    level: String,
    name: string,
    question: String,
    severity: String,
    status: String,
    title: String,
    type: String,
}

export interface Statements extends Array<Statement> {}