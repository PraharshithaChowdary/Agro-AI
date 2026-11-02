import React from 'react';
import { CheckCircle2, Info } from 'lucide-react';

type Props = {
  savedToAccount?: boolean;
  message?: string;
};

/** Makes persistence explicit: a preview is never presented as a saved account record. */
export const PersistenceNotice: React.FC<Props> = ({ savedToAccount, message }) => (
  <div
    role="status"
    className={`flex items-start gap-2 rounded-xl border px-4 py-3 text-xs ${
      savedToAccount
        ? 'border-emerald-200 bg-emerald-50 text-emerald-900'
        : 'border-amber-200 bg-amber-50 text-amber-950'
    }`}
  >
    {savedToAccount ? <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" /> : <Info className="mt-0.5 h-4 w-4 shrink-0" />}
    <span>{message || (savedToAccount ? 'Saved to your account history.' : 'Preview only. Sign in to save this result to your account.')}</span>
  </div>
);
