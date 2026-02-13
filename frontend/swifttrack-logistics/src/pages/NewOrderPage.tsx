import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '@/context/AppContext';
import { 
  ArrowLeft, 
  ArrowRight, 
  Check, 
  Package, 
  MapPin, 
  FileText,
  Plus,
  Trash2,
  AlertTriangle
} from 'lucide-react';
import { DeliveryAddress, OrderItem, Priority, Order } from '@/types';

const NewOrderPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, addOrder } = useApp();
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    deliveryAddress: {
      street: '',
      city: '',
      state: '',
      zipCode: '',
      country: 'USA',
      instructions: '',
    } as DeliveryAddress,
    items: [{ id: `item-${Date.now()}`, name: '', quantity: 1, weight: 0, price: 0 }] as OrderItem[],
    priority: 'normal' as Priority,
    specialInstructions: '',
  });

  const updateAddress = (field: keyof DeliveryAddress, value: string) => {
    setFormData(prev => ({
      ...prev,
      deliveryAddress: { ...prev.deliveryAddress, [field]: value }
    }));
  };

  const addItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { id: `item-${Date.now()}`, name: '', quantity: 1, weight: 0, price: 0 }]
    }));
  };

  const removeItem = (id: string) => {
    if (formData.items.length > 1) {
      setFormData(prev => ({
        ...prev,
        items: prev.items.filter(item => item.id !== id)
      }));
    }
  };

  const updateItem = (id: string, field: keyof OrderItem, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.map(item => 
        item.id === id ? { ...item, [field]: value } : item
      )
    }));
  };

  const totalWeight = formData.items.reduce((sum, item) => sum + (item.weight * item.quantity), 0);
  const estimatedCost = 500 + (totalWeight * 100);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    const orderNumber = `SW-${new Date().getFullYear()}-${String(Date.now()).slice(-5)}`;
    
    const newOrder: Omit<Order, 'id' | 'createdAt' | 'updatedAt'> = {
      orderNumber,
      clientId: user?.id || 'unknown',
      clientName: user?.name || 'Unknown Client',
      deliveryAddress: formData.deliveryAddress,
      items: formData.items,
      priority: formData.priority,
      specialInstructions: formData.specialInstructions || undefined,
      status: 'checking_warehouse',
      estimatedDelivery: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
    };

    addOrder(newOrder);
    navigate('/dashboard');
  };

  const priorityOptions: { value: Priority; label: string; description: string }[] = [
    { value: 'normal', label: 'Normal', description: '3-5 business days' },
    { value: 'high', label: 'High', description: '1-2 business days' },
    { value: 'urgent', label: 'Urgent', description: 'Same day delivery' },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 backdrop-blur-xl bg-background/80 border-b border-border">
        <div className="container max-w-2xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 rounded-xl hover:bg-secondary/50 text-muted-foreground hover:text-foreground transition-colors"
            >
              <ArrowLeft className="w-5 h-5" strokeWidth={1.5} />
            </button>
            <div>
              <h1 className="text-lg font-bold text-foreground">New Order</h1>
              <p className="text-xs text-muted-foreground">Step {step} of 3</p>
            </div>
          </div>
        </div>
      </header>

      <main className="container max-w-2xl mx-auto px-4 py-6">
        {/* Progress */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {[1, 2, 3].map((s) => (
            <React.Fragment key={s}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                s < step ? 'bg-success text-success-foreground' :
                s === step ? 'bg-primary text-primary-foreground shadow-glow-primary' :
                'bg-secondary text-muted-foreground'
              }`}>
                {s < step ? <Check className="w-5 h-5" strokeWidth={2} /> : 
                 s === 1 ? <MapPin className="w-4 h-4" strokeWidth={1.5} /> :
                 s === 2 ? <Package className="w-4 h-4" strokeWidth={1.5} /> :
                 <FileText className="w-4 h-4" strokeWidth={1.5} />}
              </div>
              {s < 3 && (
                <div className={`w-16 h-1 rounded-full transition-all ${
                  s < step ? 'bg-success' : 'bg-secondary'
                }`} />
              )}
            </React.Fragment>
          ))}
        </div>

        <div className="glass-card p-6">
          {/* Step 1: Delivery Address */}
          {step === 1 && (
            <div className="space-y-5 animate-fade-in">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2.5 rounded-xl bg-primary/20">
                  <MapPin className="w-5 h-5 text-primary" strokeWidth={1.5} />
                </div>
                <h2 className="text-lg font-semibold text-foreground">Delivery Address</h2>
              </div>

              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-2">Street Address</label>
                <input
                  type="text"
                  value={formData.deliveryAddress.street}
                  onChange={(e) => updateAddress('street', e.target.value)}
                  className="glass-input"
                  placeholder="123 Main Street, Suite 100"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">City</label>
                  <input
                    type="text"
                    value={formData.deliveryAddress.city}
                    onChange={(e) => updateAddress('city', e.target.value)}
                    className="glass-input"
                    placeholder="San Francisco"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">State</label>
                  <input
                    type="text"
                    value={formData.deliveryAddress.state}
                    onChange={(e) => updateAddress('state', e.target.value)}
                    className="glass-input"
                    placeholder="CA"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">ZIP Code</label>
                  <input
                    type="text"
                    value={formData.deliveryAddress.zipCode}
                    onChange={(e) => updateAddress('zipCode', e.target.value)}
                    className="glass-input"
                    placeholder="94102"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-muted-foreground mb-2">Country</label>
                  <input
                    type="text"
                    value={formData.deliveryAddress.country}
                    onChange={(e) => updateAddress('country', e.target.value)}
                    className="glass-input"
                    placeholder="USA"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-2">Delivery Instructions (Optional)</label>
                <textarea
                  value={formData.deliveryAddress.instructions}
                  onChange={(e) => updateAddress('instructions', e.target.value)}
                  className="glass-input min-h-[80px] resize-none"
                  placeholder="Leave at front door, ring doorbell, etc."
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

          {/* Step 2: Items */}
          {step === 2 && (
            <div className="space-y-5 animate-fade-in">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-primary/20">
                    <Package className="w-5 h-5 text-primary" strokeWidth={1.5} />
                  </div>
                  <h2 className="text-lg font-semibold text-foreground">Package Items</h2>
                </div>
                <button
                  type="button"
                  onClick={addItem}
                  className="btn-secondary !px-3 !min-h-[40px]"
                >
                  <Plus className="w-4 h-4" strokeWidth={1.5} />
                </button>
              </div>

              <div className="space-y-4">
                {formData.items.map((item, index) => (
                  <div key={item.id} className="p-4 rounded-xl bg-secondary/30 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-muted-foreground">Item {index + 1}</span>
                      {formData.items.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeItem(item.id)}
                          className="p-1.5 rounded-lg hover:bg-destructive/20 text-muted-foreground hover:text-destructive transition-colors"
                        >
                          <Trash2 className="w-4 h-4" strokeWidth={1.5} />
                        </button>
                      )}
                    </div>
                    
                    <input
                      type="text"
                      value={item.name}
                      onChange={(e) => updateItem(item.id, 'name', e.target.value)}
                      className="glass-input"
                      placeholder="Item name (e.g., Electronics Package)"
                      required
                    />
                    
                    <div className="grid grid-cols-3 gap-3">
                      <div>
                        <label className="block text-xs text-muted-foreground mb-1">Qty</label>
                        <input
                          type="number"
                          min="1"
                          value={item.quantity}
                          onChange={(e) => updateItem(item.id, 'quantity', parseInt(e.target.value) || 1)}
                          className="glass-input text-center"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-muted-foreground mb-1">Weight (kg)</label>
                        <input
                          type="number"
                          min="0"
                          step="0.1"
                          value={item.weight || ''}
                          onChange={(e) => updateItem(item.id, 'weight', parseFloat(e.target.value) || 0)}
                          className="glass-input text-center"
                          placeholder="0.0"
                        />
                      </div>
                      <div>
                        <label className="block text-xs text-muted-foreground mb-1">Value ($)</label>
                        <input
                          type="number"
                          min="0"
                          value={item.price || ''}
                          onChange={(e) => updateItem(item.id, 'price', parseFloat(e.target.value) || 0)}
                          className="glass-input text-center"
                          placeholder="0"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Summary */}
              <div className="p-4 rounded-xl bg-primary/10 border border-primary/20">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-muted-foreground">Total Weight</span>
                  <span className="font-semibold text-foreground">{totalWeight.toFixed(1)} kg</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Estimated Cost</span>
                  <span className="text-lg font-bold text-primary">${estimatedCost.toLocaleString()}</span>
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

          {/* Step 3: Priority & Review */}
          {step === 3 && (
            <div className="space-y-5 animate-fade-in">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2.5 rounded-xl bg-primary/20">
                  <FileText className="w-5 h-5 text-primary" strokeWidth={1.5} />
                </div>
                <h2 className="text-lg font-semibold text-foreground">Review & Submit</h2>
              </div>

              {/* Priority Selection */}
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-3">Priority Level</label>
                <div className="space-y-2">
                  {priorityOptions.map((option) => (
                    <label
                      key={option.value}
                      className={`flex items-center gap-3 p-4 rounded-xl cursor-pointer transition-all ${
                        formData.priority === option.value
                          ? option.value === 'urgent' 
                            ? 'bg-destructive/20 border-2 border-destructive'
                            : option.value === 'high'
                            ? 'bg-warning/20 border-2 border-warning'
                            : 'bg-primary/20 border-2 border-primary'
                          : 'bg-secondary/30 border-2 border-transparent hover:border-border'
                      }`}
                    >
                      <input
                        type="radio"
                        name="priority"
                        value={option.value}
                        checked={formData.priority === option.value}
                        onChange={(e) => setFormData(prev => ({ ...prev, priority: e.target.value as Priority }))}
                        className="sr-only"
                      />
                      <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                        formData.priority === option.value
                          ? option.value === 'urgent' ? 'border-destructive bg-destructive'
                            : option.value === 'high' ? 'border-warning bg-warning'
                            : 'border-primary bg-primary'
                          : 'border-muted-foreground'
                      }`}>
                        {formData.priority === option.value && (
                          <Check className="w-3 h-3 text-white" strokeWidth={3} />
                        )}
                      </div>
                      <div className="flex-1">
                        <span className="font-medium text-foreground">{option.label}</span>
                        <p className="text-xs text-muted-foreground">{option.description}</p>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Special Instructions */}
              <div>
                <label className="block text-sm font-medium text-muted-foreground mb-2">Special Instructions (Optional)</label>
                <textarea
                  value={formData.specialInstructions}
                  onChange={(e) => setFormData(prev => ({ ...prev, specialInstructions: e.target.value }))}
                  className="glass-input min-h-[100px] resize-none"
                  placeholder="Any special handling requirements, fragile items, etc."
                />
              </div>

              {/* Order Summary */}
              <div className="p-4 rounded-xl bg-secondary/30 space-y-3">
                <h4 className="font-medium text-foreground">Order Summary</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Delivery to</span>
                    <span className="text-foreground">{formData.deliveryAddress.city}, {formData.deliveryAddress.state}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Items</span>
                    <span className="text-foreground">{formData.items.length} package(s)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Total Weight</span>
                    <span className="text-foreground">{totalWeight.toFixed(1)} kg</span>
                  </div>
                  <div className="flex justify-between pt-2 border-t border-border">
                    <span className="font-medium text-foreground">Total Cost</span>
                    <span className="text-lg font-bold text-primary">${estimatedCost.toLocaleString()}</span>
                  </div>
                </div>
              </div>

              {formData.priority === 'urgent' && (
                <div className="flex items-start gap-3 p-3 rounded-xl bg-warning/10 border border-warning/20">
                  <AlertTriangle className="w-5 h-5 text-warning shrink-0 mt-0.5" strokeWidth={1.5} />
                  <p className="text-sm text-foreground">
                    Urgent priority incurs additional rush fees and is subject to driver availability.
                  </p>
                </div>
              )}

              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setStep(2)}
                  className="btn-secondary flex-1"
                >
                  <ArrowLeft className="w-5 h-5" strokeWidth={1.5} /> Back
                </button>
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  className="btn-success flex-1"
                >
                  {isSubmitting ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Submitting...
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      Submit Order <Check className="w-5 h-5" strokeWidth={1.5} />
                    </span>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default NewOrderPage;
