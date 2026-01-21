import type { Metadata } from 'next'
import { Toaster } from 'sonner'
import ThemeProvider from '@/components/ThemeProvider'
import './globals.css'

export const metadata: Metadata = {
  title: 'Mira Intel - Offshore Wind Damage Detection',
  description: 'AI-powered wind turbine blade damage detection system',
  icons: {
    icon: '/img/favicon.ico',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'var(--toast-bg, #fff)',
                color: 'var(--toast-color, #333)',
                border: '1px solid var(--toast-border, #e5e7eb)',
              },
            }}
            richColors
            closeButton
          />
        </ThemeProvider>
      </body>
    </html>
  )
}

