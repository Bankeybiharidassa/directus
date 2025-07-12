export default {
  collections: [
    {
      collection: 'nucleus_auth_tokens',
      fields: [
        { field: 'id', type: 'uuid', primaryKey: true },
        { field: 'user', type: 'uuid' },
        { field: 'token', type: 'string' }
      ]
    }
  ]
};
