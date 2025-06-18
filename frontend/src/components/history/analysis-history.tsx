'use client';

import React, { useState, useEffect } from 'react';
import { offlineStorage, AnalysisRecord } from '@/lib/offline-storage';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  History, 
  Trash2, 
  Eye, 
  Download, 
  Calendar,
  Clock,
  User,
  Palette,
  HardDrive,
  RefreshCw
} from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import EnhancedResults from '@/components/analyze/enhanced-results';

interface AnalysisHistoryProps {
  onSelectAnalysis?: (analysis: AnalysisRecord) => void;
}

const AnalysisHistory: React.FC<AnalysisHistoryProps> = ({ onSelectAnalysis }) => {
  const [analyses, setAnalyses] = useState<AnalysisRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAnalysis, setSelectedAnalysis] = useState<AnalysisRecord | null>(null);
  const [storageUsage, setStorageUsage] = useState<{ used: number; quota: number }>({ used: 0, quota: 0 });

  useEffect(() => {
    loadAnalyses();
    loadStorageUsage();
  }, []);

  const loadAnalyses = async () => {
    try {
      setLoading(true);
      const allAnalyses = await offlineStorage.getAllAnalyses();
      setAnalyses(allAnalyses);
      setError(null);
    } catch (err) {
      setError('Failed to load analysis history');
      console.error('Error loading analyses:', err);
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

  const handleDeleteAnalysis = async (id: string) => {
    if (!confirm('Are you sure you want to delete this analysis? This action cannot be undone.')) {
      return;
    }

    try {
      await offlineStorage.deleteAnalysis(id);
      setAnalyses(prev => prev.filter(analysis => analysis.id !== id));
      if (selectedAnalysis?.id === id) {
        setSelectedAnalysis(null);
      }
      await loadStorageUsage();
    } catch (err) {
      setError('Failed to delete analysis');
      console.error('Error deleting analysis:', err);
    }
  };

  const handleViewAnalysis = (analysis: AnalysisRecord) => {
    setSelectedAnalysis(analysis);
    onSelectAnalysis?.(analysis);
  };

  const handleExportAnalysis = (analysis: AnalysisRecord) => {
    const dataStr = JSON.stringify(analysis, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `chromalyze-analysis-${analysis.id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleClearOldData = async () => {
    if (!confirm('This will delete analyses older than 30 days. Continue?')) {
      return;
    }

    try {
      await offlineStorage.clearOldData(30);
      await loadAnalyses();
      await loadStorageUsage();
    } catch (err) {
      setError('Failed to clear old data');
      console.error('Error clearing old data:', err);
    }
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
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

  if (selectedAnalysis) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Button 
            variant="outline" 
            onClick={() => setSelectedAnalysis(null)}
            className="mb-4"
          >
            ← Back to History
          </Button>
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => handleExportAnalysis(selectedAnalysis)}
            >
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
            <Button 
              variant="destructive" 
              size="sm"
              onClick={() => handleDeleteAnalysis(selectedAnalysis.id)}
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Delete
            </Button>
          </div>
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <History className="h-5 w-5" />
              Analysis from {formatDate(selectedAnalysis.timestamp)}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="text-center">
                <Clock className="h-6 w-6 mx-auto mb-2 text-blue-500" />
                <p className="text-sm text-gray-600">Processing Time</p>
                <p className="font-semibold">{Math.round(selectedAnalysis.result.processingTime)}ms</p>
              </div>
              <div className="text-center">
                <HardDrive className="h-6 w-6 mx-auto mb-2 text-green-500" />
                <p className="text-sm text-gray-600">Image Size</p>
                <p className="font-semibold">{formatBytes(selectedAnalysis.metadata.imageSize)}</p>
              </div>
              <div className="text-center">
                <Badge variant="secondary" className="text-sm">
                  v{selectedAnalysis.metadata.version}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <EnhancedResults results={selectedAnalysis.result} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <History className="h-6 w-6" />
            Analysis History
          </h2>
          <p className="text-gray-600 mt-1">
            View and manage your saved analysis results
          </p>
        </div>
        <Button onClick={loadAnalyses} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Storage Usage */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <HardDrive className="h-5 w-5" />
            Storage Usage
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span>Used: {formatBytes(storageUsage.used)}</span>
              <span>Available: {formatBytes(storageUsage.quota)}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full transition-all duration-300 ${
                  getStoragePercentage() > 80 ? 'bg-red-500' :
                  getStoragePercentage() > 60 ? 'bg-yellow-500' : 'bg-green-500'
                }`}
                style={{ width: `${Math.min(getStoragePercentage(), 100)}%` }}
              ></div>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">
                {getStoragePercentage().toFixed(1)}% used
              </span>
              <Button 
                variant="outline" 
                size="sm"
                onClick={handleClearOldData}
                disabled={analyses.length === 0}
              >
                Clear Old Data
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-8">
          <RefreshCw className="h-6 w-6 animate-spin mr-2" />
          <span>Loading analysis history...</span>
        </div>
      )}

      {/* Empty State */}
      {!loading && analyses.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <History className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <h3 className="text-lg font-semibold mb-2">No Analysis History</h3>
            <p className="text-gray-600 mb-4">
              Your saved analysis results will appear here
            </p>
            <Button onClick={() => window.location.href = '/analyze'}>
              Start New Analysis
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Analysis List */}
      {!loading && analyses.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {analyses.map((analysis) => (
            <Card key={analysis.id} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    {formatDate(analysis.timestamp)}
                  </CardTitle>
                  <Badge variant="secondary" className="text-xs">
                    {Math.round(analysis.result.confidence * 100)}%
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <User className="h-4 w-4 text-blue-500" />
                    <div>
                      <p className="font-medium">Face Shape</p>
                      <p className="text-gray-600 capitalize">
                        {analysis.result.faceShape.faceShape}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Palette className="h-4 w-4 text-purple-500" />
                    <div>
                      <p className="font-medium">Color Season</p>
                      <p className="text-gray-600 capitalize">
                        {analysis.result.colorSeason.season.replace('_', ' ')}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="flex-1"
                    onClick={() => handleViewAnalysis(analysis)}
                  >
                    <Eye className="h-4 w-4 mr-2" />
                    View
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => handleExportAnalysis(analysis)}
                  >
                    <Download className="h-4 w-4" />
                  </Button>
                  <Button 
                    variant="destructive" 
                    size="sm"
                    onClick={() => handleDeleteAnalysis(analysis.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default AnalysisHistory;
