export interface Statement {
    area: String,
    company: Number,
    description: string,
    id: number,
    level: String,
    name: string,
    question: String,
    severity: String,
    status: String,
    title: string,
    type: String,
}

export interface Statements extends Array<Statement> {}