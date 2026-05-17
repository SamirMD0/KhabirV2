import { client } from './client'

export const casesApi = {
  upload: (formData) =>
    client.post('/api/cases/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(r => r.data),

  analyze: (caseId) =>
    client.post(`/api/cases/${caseId}/analyze`).then(r => r.data),

  get: (caseId) =>
    client.get(`/api/cases/${caseId}`).then(r => r.data),

  getSimilar: (caseId) =>
    client.get(`/api/cases/${caseId}/similar`).then(r => r.data),

  delete: (caseId) =>
    client.delete(`/api/cases/${caseId}`).then(r => r.data),

  chat: (caseId, message) =>
    client.post(`/api/cases/${caseId}/chat`, { message }).then(r => r.data),
}
