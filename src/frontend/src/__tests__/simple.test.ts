import { describe, test, expect } from 'vitest'

describe('Simple Tests', () => {
  test('basic functionality works', () => {
    expect(1 + 1).toBe(2)
  })

  test('string operations work', () => {
    expect('hello'.toUpperCase()).toBe('HELLO')
  })

  test('array operations work', () => {
    const arr = [1, 2, 3]
    expect(arr.length).toBe(3)
    expect(arr.includes(2)).toBe(true)
  })
})