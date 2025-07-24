'use client';

import React, { useState, useEffect } from 'react';
import { offlineStorage, UserPreferences } from '@/lib/offline-storage';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { 
  Settings, 
  Database, 
  Shield, 
  Zap, 
  Save,
  RefreshCw,
  Trash2,
  HardDrive
} from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

const PreferencesComponent: React.FC = () => {
  const [preferences, setPreferences] = useState<UserPreferences>({
    id: 'user_preferences',
    theme: 'auto',
    language: 'en',
    analysisSettings: {
      useEnhancedAnalysis: true,
      saveResults: true,
      autoAnalyze: false
    },
    privacy: {
      saveImages: true,
      shareAnalytics: false
    }
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [storageUsage, setStorageUsage] = useState<{ used: number; quota: number }>({ used: 0, quota: 0 });

  useEffect(() => {
    loadPreferences();
    loadStorageUsage();
  }, []);

  const loadPreferences = async () => {
    try {
      setLoading(true);
      const savedPreferences = await offlineStorage.getPreferences();
      if (savedPreferences) {
        setPreferences(savedPreferences);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load preferences');
      console.error('Error loading preferences:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadStorageUsage = async () => {
    try {
      const usage = await offlineStorage.getStorageUsage();
      setStorageUsage(usage);
    } catch (err) {
      console.error('Error loading storage usage:', err);
    }
  };

  const savePreferences = async () => {
    try {
      setSaving(true);
      await offlineStorage.savePreferences(preferences);
      setSuccess('Preferences saved successfully');
      setError(null);
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to save preferences');
      console.error('Error saving preferences:', err);
    } finally {
      setSaving(false);
    }
  };

  const clearAllData = async () => {
    if (!confirm('This will delete ALL your saved analyses and images. This action cannot be undone. Continue?')) {
      return;
    }

    try {
      // Clear all data by clearing old data with 0 days
      await offlineStorage.clearOldData(0);
      await loadStorageUsage();
      setSuccess('All data cleared successfully');
    } catch (err) {
      setError('Failed to clear data');
      console.error('Error clearing data:', err);
    }
  };

  const updatePreference = (section: keyof UserPreferences, key: string, value: any) => {
    setPreferences(prev => ({
      ...prev,
      [section]: {
        ...(prev[section] as any || {}),
        [key]: value
      }
    }));
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStoragePercentage = () => {
    if (storageUsage.quota === 0) return 0;
    return (storageUsage.used / storageUsage.quota) * 100;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <RefreshCw className="h-6 w-6 animate-spin mr-2" />
        <span>Loading preferences...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Settings className="h-6 w-6" />
            Preferences
          </h2>
          <p className="text-gray-600 mt-1">
            Manage your analysis settings and data storage
          </p>
        </div>
        <Button onClick={savePreferences} disabled={saving}>
          {saving ? (
            <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
          ) : (
            <Save className="h-4 w-4 mr-2" />
          )}
          Save Changes
        </Button>
      </div>

      {/* Alerts */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="border-green-500 bg-green-50 text-green-800">
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      )}

      {/* Analysis Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5" />
            Analysis Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="enhanced-analysis">Enhanced Analysis</Label>
              <p className="text-sm text-gray-600">
                Use advanced AI models for more accurate results
              </p>
            </div>
            <Switch
              id="enhanced-analysis"
              checked={preferences.analysisSettings.useEnhancedAnalysis}
              onCheckedChange={(checked) => 
                updatePreference('analysisSettings', 'useEnhancedAnalysis', checked)
              }
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="save-results">Save Results</Label>
              <p className="text-sm text-gray-600">
                Automatically save analysis results for offline access
              </p>
            </div>
            <Switch
              id="save-results"
              checked={preferences.analysisSettings.saveResults}
              onCheckedChange={(checked) => 
                updatePreference('analysisSettings', 'saveResults', checked)
              }
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="auto-analyze">Auto Analyze</Label>
              <p className="text-sm text-gray-600">
                Start analysis automatically when image is uploaded
              </p>
            </div>
            <Switch
              id="auto-analyze"
              checked={preferences.analysisSettings.autoAnalyze}
              onCheckedChange={(checked) => 
                updatePreference('analysisSettings', 'autoAnalyze', checked)
              }
            />
          </div>
        </CardContent>
      </Card>

      {/* Privacy Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Privacy Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="save-images">Save Images Locally</Label>
              <p className="text-sm text-gray-600">
                Store uploaded images in your browser for offline access
              </p>
            </div>
            <Switch
              id="save-images"
              checked={preferences.privacy.saveImages}
              onCheckedChange={(checked) => 
                updatePreference('privacy', 'saveImages', checked)
              }
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label htmlFor="share-analytics">Share Analytics</Label>
              <p className="text-sm text-gray-600">
                Help improve the app by sharing anonymous usage data
              </p>
            </div>
            <Switch
              id="share-analytics"
              checked={preferences.privacy.shareAnalytics}
              onCheckedChange={(checked) => 
                updatePreference('privacy', 'shareAnalytics', checked)
              }
            />
          </div>
        </CardContent>
      </Card>

      {/* Storage Management */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Storage Management
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span>Used: {formatBytes(storageUsage.used)}</span>
              <span>Available: {formatBytes(storageUsage.quota)}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div 
                className={`h-3 rounded-full transition-all duration-300 ${
                  getStoragePercentage() > 80 ? 'bg-red-500' :
                  getStoragePercentage() > 60 ? 'bg-yellow-500' : 'bg-green-500'
                }`}
                style={{ width: `${Math.min(getStoragePercentage(), 100)}%` }}
              ></div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">
                {getStoragePercentage().toFixed(1)}% used
              </span>
              <Button 
                variant="outline" 
                size="sm"
                onClick={loadStorageUsage}
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>
          </div>

          <div className="pt-4 border-t">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-red-600">Danger Zone</h4>
                <p className="text-sm text-gray-600">
                  Permanently delete all stored data
                </p>
              </div>
              <Button 
                variant="destructive" 
                onClick={clearAllData}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Clear All Data
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PreferencesComponent;
