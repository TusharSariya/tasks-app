import { TASK_STATE_COLORS, DEFAULT_STATE_COLOR } from './taskConstants'

export const getStateColor = (state) => {
  return TASK_STATE_COLORS[state?.toLowerCase()] || DEFAULT_STATE_COLOR
}

export const getStateLabel = (state) => {
  return state?.charAt(0).toUpperCase() + state.slice(1) || ''
}

export const groupTasksByHeadline = (data) => {
  const grouped = data.reduce((acc, item) => {
    const headline = item.Headline
    if (!acc[headline]) {
      acc[headline] = {
        headline: headline,
        state: item.State,
        authors: [],
        comments: item.comments || []
      }
    }
    if (!acc[headline].authors.includes(item.Author)) {
      acc[headline].authors.push(item.Author)
    }
    return acc
  }, {})
  
  return Object.values(grouped)
}