import { render, screen, act, waitFor } from '@testing-library/react'
import AnalysisClient from '../analysis-client'

// Mock the useRouter hook
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}))

// Mock fetch API
const mockFetch = jest.fn()
global.fetch = mockFetch as typeof global.fetch

describe('AnalysisClient', () => {
  beforeEach(() => {
    mockFetch.mockClear()
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.useRealTimers()
  })

  it('renders loading state initially', async () => {
    mockFetch.mockImplementation(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: new Headers(),
        redirected: false,
        type: 'basic' as ResponseType,
        url: 'http://localhost:8000',
        json: () => Promise.resolve({ status: 'pending' })
      } as Response)
    )

    await act(async () => {
      render(<AnalysisClient analysisId="test-id" />)
    })
    expect(screen.getByText(/Analyzing image/i)).toBeInTheDocument()
    expect(screen.getByText(/Please wait while we analyze your photo/i)).toBeInTheDocument()
  })

  it('displays results when analysis is complete', async () => {
    const mockResults = {
      faces_detected: 1,
      skin_tone: 'Warm',
      face_shape: 'Oval',
      color_season: 'Spring'
    }

    mockFetch.mockImplementation(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: new Headers(),
        redirected: false,
        type: 'basic' as ResponseType,
        url: 'http://localhost:8000',
        json: () => Promise.resolve({ status: 'completed', results: mockResults })
      } as Response)
    )

    await act(async () => {
      render(<AnalysisClient analysisId="test-id" />)
    })

    expect(screen.getByText('Color Season: Spring')).toBeInTheDocument()
    expect(screen.getByText('Warm')).toBeInTheDocument()
    expect(screen.getByText('Oval')).toBeInTheDocument()
  })

  it('handles errors gracefully', async () => {
    mockFetch.mockImplementation(() =>
      Promise.reject(new Error('Network error'))
    )

    await act(async () => {
      render(<AnalysisClient analysisId="test-id" />)
    })

    expect(screen.getByText(/Analysis Failed/i)).toBeInTheDocument()
    expect(screen.getByText(/Network error/i)).toBeInTheDocument()
  })

  it('shows progress during analysis', async () => {
    const mockResults = {
      faces_detected: 1,
      skin_tone: 'Warm',
      face_shape: 'Oval',
      color_season: 'Spring'
    }

    let resolvePromise: (value: any) => void
    const pendingPromise = new Promise(resolve => {
      resolvePromise = resolve
    })

    mockFetch.mockImplementation(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: new Headers(),
        redirected: false,
        type: 'basic' as ResponseType,
        url: 'http://localhost:8000',
        json: () => pendingPromise
      } as Response)
    )

    await act(async () => {
      render(<AnalysisClient analysisId="test-id" />)
    })

    await act(async () => {
      resolvePromise!({ status: 'pending' })
    })

    expect(screen.getByText(/Analyzing image/i)).toBeInTheDocument()
    expect(screen.getByText(/Please wait while we analyze your photo/i)).toBeInTheDocument()

    // Change mock to return completed status
    mockFetch.mockImplementation(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        statusText: 'OK',
        headers: new Headers(),
        redirected: false,
        type: 'basic' as ResponseType,
        url: 'http://localhost:8000',
        json: () => Promise.resolve({ status: 'completed', results: mockResults })
      } as Response)
    )

    await act(async () => {
      jest.advanceTimersByTime(2000)
      await Promise.resolve()
    })

    await waitFor(() => {
      expect(screen.getByText(/Warm/i)).toBeInTheDocument()
    })
  })

  it('handles server errors with error message', async () => {
    mockFetch.mockImplementation(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        headers: new Headers(),
        redirected: false,
        type: 'basic' as ResponseType,
        url: 'http://localhost:8000',
        json: () => Promise.resolve({ error: 'Internal Server Error' })
      } as Response)
    )

    await act(async () => {
      render(<AnalysisClient analysisId="test-id" />)
    })

    expect(screen.getByText(/Analysis Failed/i)).toBeInTheDocument()
    expect(screen.getByText(/HTTP error! status: 500/i)).toBeInTheDocument()
  })
}) 