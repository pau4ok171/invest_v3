// Utilities
import { onUnmounted, ref } from 'vue'

interface WebsocketOptions {
  url: string
  maxReconnectAttempts?: number
  reconnectInterval?: number
  onMessage?: (data: any) => void
  onOpen?: () => void
  onError?: (error: Error) => void
}

export const useWebsocket = (options: WebsocketOptions) => {
  const socket = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const reconnectAttempts = ref(0)
  const reconnectTimer = ref<number | null>(null)
  const error = ref<Error | null>(null)

  const connect = () => {

    try {
      const timer = setTimeout(() => {
        if (socket.value?.readyState === WebSocket.CONNECTING) {
          console.warn('[WebSocket] Connection timeout')
          socket.value.close()
          reconnect()
        }
      }, 5000)

      socket.value = new WebSocket(options.url)

      socket.value.onopen = () => {
        clearTimeout(timer)
        console.log('[WebSocket] Connection established')
        isConnected.value = true
        reconnectAttempts.value = 0
        options.onOpen?.()
      }

      socket.value.onerror = (event) => {
        clearTimeout(timer)
        console.error('[WebSocket] Error:', event)
        error.value = new Error('WebSocket error')
        options.onError?.(error.value)
        socket.value?.close()
      }

      socket.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          options.onMessage?.(data)
        } catch (e) {
          console.error('Error parsing WebSocket message:', e)
        }
      }

      socket.value.onclose = (event) => {
        isConnected.value = false
        if (event.code !== 1000) {
          reconnect()
        }
      }
    } catch (e) {
      console.error('[WebSocket] Connection error:', e)
      reconnect()
    }
  }

  const reconnect = () => {
    if (reconnectAttempts.value < (options.maxReconnectAttempts || 5)) {
      reconnectAttempts.value++
      reconnectTimer.value = window.setTimeout(
        () => {
          connect()
        },
        (options.reconnectInterval || 3000) *
          Math.pow(1.5, reconnectAttempts.value)
      )
    }
  }

  const send = (data: any) => {
    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify(data))
    }
  }

  const close = (code?: number, reason?: string) => {
    if (reconnectTimer.value) {
      clearTimeout(reconnectTimer.value)
    }
    socket.value?.close(code || 1000, reason)
  }

  onUnmounted(() => {
    close()
  })

  return {
    isConnected,
    error,
    connect,
    send,
    close,
  }
}
