export default function register({ services }) {
  const { logger } = services;
  logger.info('Nucleus Core extension loaded');
}
