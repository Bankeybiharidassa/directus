# fix-phase3-pass16
Built @directus/random and @directus/storage packages under Node 18.
Added fs.glob polyfill loaded via NODE_OPTIONS for test runs.
Monorepo tests now progress beyond missing module errors but still fail due to fs.glob not supporting recursive patterns.
