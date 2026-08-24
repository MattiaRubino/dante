import { AccessPage } from '../features/access';
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/')({
  component: AccessPage,
});
