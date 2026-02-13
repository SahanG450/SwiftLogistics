import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useApp } from '@/context/AppContext';
import { Truck, ArrowRight, ArrowLeft, Check } from 'lucide-react';

const RegisterPage: React.FC = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    membership_level: 'silver' as 'gold' | 'silver' | 'platinum',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useApp();
  const navigate = useNavigate();

  const updateField = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      const success = await register(formData);
      if (success) {
        navigate('/dashboard');
      } else {
        setError('Registration failed. Please try again.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const membershipOptions = [
    { value: 'silver', label: 'Silver', price: '$99/mo', features: ['Up to 50 deliveries', 'Standard support', 'Basic tracking'] },
    { value: 'gold', label: 'Gold', price: '$199/mo', features: ['Up to 200 deliveries', 'Priority support', 'Advanced tracking'] },
    { value: 'platinum', label: 'Platinum', price: '$499/mo', features: ['Unlimited deliveries', '24/7 support', 'Premium features'] },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      {/* Background */}
      <div className="fixed inset-0 bg-gradient-to-br from-background via-card to-background -z-10" />
      <div className="fixed top-1/4 right-1/4 w-96 h-96 bg-success/10 rounded-full blur-3xl -z-10" />
      <div className="fixed bottom-1/4 left-1/4 w-96 h-96 bg-primary/15 rounded-full blur-3xl -z-10" />

      <div className="w-full max-w-lg animate-slide-up">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-accent mb-4 shadow-glow-primary">
            <Truck className="w-8 h-8 text-primary-foreground" strokeWidth={1.5} />
          </Link>
          <h1 className="text-2xl font-bold text-foreground">Create Account</h1>
          <p className="text-muted-foreground mt-1">Join SwiftTrack today</p>
        </div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {[1, 2, 3].map((s) => (
            <React.Fragment key={s}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all ${
                s < step ? 'bg-success text-success-foreground' :
                s === step ? 'bg-primary text-primary-foreground shadow-glow-primary' :
                'bg-secondary text-muted-foreground'
              }`}>
                {s < step ? <Check className="w-5 h-5" strokeWidth={2} /> : s}
              </div>
              {s < 3 && (
                <div className={`w-12 h-1 rounded-full transition-all ${
                  s < step ? 'bg-success' : 'bg-secondary'
                }`} />
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Form Card */}
        <div className="glass-card p-8">
          <form onSubmit={handleSubmit}>
            {error && (
              <div className="mb-5 p-4 rounded-xl bg-destructive/20 border border-destructive/30 text-destructive text-sm animate-fade-in">
                {error}
              </div>
            )}

            {/* Step 1: Personal Info */}
            {step === 1 && (
              <div className="space-y-5 animate-fade-in">
                <h3 className="text-lg font-semibold text-foreground mb-4">Personal Information</h3>
                
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Full Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => updateField('name', e.target.value)}
                    className="glass-input"
                    placeholder="John Doe"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Email Address</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => updateField('email', e.target.value)}
                    className="glass-input"
                    placeholder="john@company.com"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Phone Number</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => updateField('phone', e.target.value)}
                    className="glass-input"
                    placeholder="+1 (555) 123-4567"
                    required
                  />
                </div>

                <button
                  type="button"
                  onClick={() => setStep(2)}
                  className="btn-primary w-full mt-6"
                >
                  Continue <ArrowRight className="w-5 h-5" strokeWidth={1.5} />
                </button>
              </div>
            )}

            {/* Step 2: Business Info */}
            {step === 2 && (
              <div className="space-y-5 animate-fade-in">
                <h3 className="text-lg font-semibold text-foreground mb-4">Business Address</h3>
                
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Business Address</label>
                  <textarea
                    value={formData.address}
                    onChange={(e) => updateField('address', e.target.value)}
                    className="glass-input min-h-[100px] resize-none"
                    placeholder="123 Business Park, Suite 100&#10;San Francisco, CA 94102"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-3">Membership Level</label>
                  <div className="space-y-3">
                    {membershipOptions.map((option) => (
                      <label
                        key={option.value}
                        className={`block p-4 rounded-xl cursor-pointer transition-all ${
                          formData.membership_level === option.value
                            ? 'bg-primary/20 border-2 border-primary'
                            : 'bg-secondary/30 border-2 border-transparent hover:border-border'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <input
                            type="radio"
                            name="membership"
                            value={option.value}
                            checked={formData.membership_level === option.value}
                            onChange={(e) => updateField('membership_level', e.target.value)}
                            className="sr-only"
                          />
                          <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                            formData.membership_level === option.value
                              ? 'border-primary bg-primary'
                              : 'border-muted-foreground'
                          }`}>
                            {formData.membership_level === option.value && (
                              <Check className="w-3 h-3 text-primary-foreground" strokeWidth={3} />
                            )}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <span className="font-medium text-foreground">{option.label}</span>
                              <span className="text-primary font-semibold">{option.price}</span>
                            </div>
                            <p className="text-xs text-muted-foreground mt-1">{option.features.join(' • ')}</p>
                          </div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="flex gap-3 mt-6">
                  <button
                    type="button"
                    onClick={() => setStep(1)}
                    className="btn-secondary flex-1"
                  >
                    <ArrowLeft className="w-5 h-5" strokeWidth={1.5} /> Back
                  </button>
                  <button
                    type="button"
                    onClick={() => setStep(3)}
                    className="btn-primary flex-1"
                  >
                    Continue <ArrowRight className="w-5 h-5" strokeWidth={1.5} />
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Password */}
            {step === 3 && (
              <div className="space-y-5 animate-fade-in">
                <h3 className="text-lg font-semibold text-foreground mb-4">Create Password</h3>
                
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Password</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => updateField('password', e.target.value)}
                    className="glass-input"
                    placeholder="Create a strong password"
                    required
                    minLength={8}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Confirm Password</label>
                  <input
                    type="password"
                    value={formData.confirmPassword}
                    onChange={(e) => updateField('confirmPassword', e.target.value)}
                    className="glass-input"
                    placeholder="Confirm your password"
                    required
                    minLength={8}
                  />
                </div>

                <div className="flex gap-3 mt-6">
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="btn-secondary flex-1"
                  >
                    <ArrowLeft className="w-5 h-5" strokeWidth={1.5} /> Back
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="btn-success flex-1"
                  >
                    {isLoading ? (
                      <span className="flex items-center gap-2">
                        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Creating...
                      </span>
                    ) : (
                      <span className="flex items-center gap-2">
                        Create Account <Check className="w-5 h-5" strokeWidth={1.5} />
                      </span>
                    )}
                  </button>
                </div>
              </div>
            )}
          </form>

          <div className="mt-6 pt-6 border-t border-border">
            <p className="text-center text-muted-foreground text-sm">
              Already have an account?{' '}
              <Link to="/login" className="text-primary hover:text-accent transition-colors font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
