import passport from 'passport';
import { Strategy as OAuth2Strategy } from 'passport-oauth2';

export default function register({ services }) {
  const { logger } = services;

  const strategy = new OAuth2Strategy(
    {
      authorizationURL: process.env.OAUTH_AUTH_URL,
      tokenURL: process.env.OAUTH_TOKEN_URL,
      clientID: process.env.NUCLEUS_CLIENT_ID,
      clientSecret: process.env.NUCLEUS_SECRET,
      callbackURL: process.env.OAUTH_CALLBACK_URL,
    },
    function verify(accessToken, refreshToken, profile, done) {
      return done(null, profile);
    }
  );

  passport.use('nucleus-oauth', strategy);
  logger.info('Nucleus OAuth2 extension loaded');
}
