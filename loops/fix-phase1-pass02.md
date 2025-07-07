# fix-phase1-pass02
After upgrading to Node 22 and running pnpm install, `npm test` still fails due to vitest missing dependencies in Directus packages.
Used apt-based NodeSource repo to install Node 22, still fails.
Further investigation needed to get vitest and @directus/random working.
