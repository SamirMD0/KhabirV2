// TODO Phase 2: fetch case by id, display analysis + chat
import { useParams } from 'react-router-dom'

export default function ResultPage() {
  const { id } = useParams()
  return (
    <main className="max-w-4xl mx-auto px-4 py-16">
      <h1 className="text-2xl font-semibold mb-2">Case #{id}</h1>
      <p className="text-neutral-400">Analysis result - Phase 2</p>
    </main>
  )
}
