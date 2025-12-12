import { useState } from 'react'
import axios from 'axios'
import './App.css'

interface QueryResponse {
  answer: string
  confidence: number
  sources: string[]
  suggestions: string[]
  related_topics: string[]
}

function App() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<QueryResponse | null>(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!query.trim()) {
      setError('Please enter a question')
      return
    }

    setLoading(true)
    setError('')
    setResponse(null)

    try {
      const result = await axios.post<QueryResponse>('/api/query', {
        query,
        context: { version: '13' }
      })
      
      setResponse(result.data)
    } catch (err) {
      setError('Failed to get response. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Cubase Expert System
          </h1>
          <p className="text-gray-400 text-lg">
            AI-powered troubleshooting and workflow optimization
          </p>
        </header>

        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask me anything about Cubase..."
              className="flex-1 px-6 py-4 rounded-lg bg-gray-800 border border-gray-700 focus:border-blue-500 focus:outline-none text-white placeholder-gray-500"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-lg font-semibold transition-colors"
            >
              {loading ? 'Thinking...' : 'Ask'}
            </button>
          </div>
        </form>

        {error && (
          <div className="bg-red-900/50 border border-red-700 rounded-lg p-4 mb-8">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {response && (
          <div className="space-y-6">
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold">Answer</h2>
                <span className="text-sm bg-blue-600 px-3 py-1 rounded-full">
                  {Math.round(response.confidence * 100)}% confident
                </span>
              </div>
              <p className="text-gray-300 leading-relaxed">{response.answer}</p>
            </div>

            {response.suggestions.length > 0 && (
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h3 className="text-xl font-semibold mb-4">Suggestions</h3>
                <ul className="space-y-2">
                  {response.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <span className="text-blue-400 mt-1">→</span>
                      <span className="text-gray-300">{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {response.related_topics.length > 0 && (
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <h3 className="text-xl font-semibold mb-4">Related Topics</h3>
                <div className="flex flex-wrap gap-2">
                  {response.related_topics.map((topic, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-gray-700 rounded-full text-sm text-gray-300"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <footer className="mt-16 text-center text-gray-500 text-sm">
          <p>Powered by AI • Built with React & FastAPI</p>
        </footer>
      </div>
    </div>
  )
}

export default App
