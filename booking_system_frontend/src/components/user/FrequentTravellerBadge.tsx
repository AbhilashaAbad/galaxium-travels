import type { User } from '../../types';

interface FrequentTravellerBadgeProps {
  user: User;
  showDetails?: boolean;
}

const statusConfig = {
  standard: {
    label: 'Standard',
    color: 'bg-gray-500',
    icon: '⭐',
    description: '0-4 bookings'
  },
  bronze: {
    label: 'Bronze',
    color: 'bg-amber-700',
    icon: '🥉',
    description: '5-9 bookings'
  },
  silver: {
    label: 'Silver',
    color: 'bg-gray-400',
    icon: '🥈',
    description: '10-19 bookings'
  },
  gold: {
    label: 'Gold',
    color: 'bg-yellow-500',
    icon: '🥇',
    description: '20-49 bookings'
  },
  platinum: {
    label: 'Platinum',
    color: 'bg-purple-500',
    icon: '💎',
    description: '50+ bookings'
  }
};

export const FrequentTravellerBadge = ({ user, showDetails = false }: FrequentTravellerBadgeProps) => {
  const status = user.frequent_traveller_status?.toLowerCase() || 'standard';
  const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.standard;

  return (
    <div className="inline-flex items-center gap-2">
      <div className={`${config.color} text-white px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-1.5 shadow-lg`}>
        <span>{config.icon}</span>
        <span>{config.label}</span>
      </div>
      
      {showDetails && (
        <div className="text-sm text-star-white/70">
          <div>{config.description}</div>
          <div className="font-semibold">{user.total_bookings} total bookings</div>
          {user.seat_preference && (
            <div className="text-cosmic-purple">
              Prefers: {user.seat_preference} seat
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Made with Bob