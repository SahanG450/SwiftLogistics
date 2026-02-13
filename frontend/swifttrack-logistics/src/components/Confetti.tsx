import React from 'react';

interface ConfettiProps {
  show: boolean;
}

const Confetti: React.FC<ConfettiProps> = ({ show }) => {
  if (!show) return null;

  const colors = ['#007AFF', '#34C759', '#FF9F0A', '#FF3B30', '#AF52DE', '#5AC8FA'];
  const confettiPieces = Array.from({ length: 50 }, (_, i) => ({
    id: i,
    left: `${Math.random() * 100}%`,
    delay: `${Math.random() * 2}s`,
    duration: `${2 + Math.random() * 2}s`,
    color: colors[Math.floor(Math.random() * colors.length)],
    size: 8 + Math.random() * 8,
    rotation: Math.random() * 360,
  }));

  return (
    <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      {confettiPieces.map((piece) => (
        <div
          key={piece.id}
          className="absolute animate-confetti"
          style={{
            left: piece.left,
            top: '-20px',
            animationDelay: piece.delay,
            animationDuration: piece.duration,
          }}
        >
          <div
            style={{
              width: piece.size,
              height: piece.size,
              backgroundColor: piece.color,
              transform: `rotate(${piece.rotation}deg)`,
              borderRadius: Math.random() > 0.5 ? '50%' : '2px',
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default Confetti;
