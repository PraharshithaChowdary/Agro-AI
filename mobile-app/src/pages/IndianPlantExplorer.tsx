import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  Search,
  Camera,
  Upload,
  AlertCircle,
  CheckCircle2,
  AlertTriangle,
  Loader2,
  Droplets,
  Sun,
  Layers,
  Sparkles,
  ShieldAlert,
  ShieldCheck,
  BookOpen,
  ExternalLink,
  ChevronRight,
  Filter,
  Eye,
  HeartPulse,
  X,
  Languages,
  Check,
  User
} from 'lucide-react';
import { plantService } from '../services/plantService';
import { PersistenceNotice } from '../components/PersistenceNotice';
import {
  PlantSummaryItem,
  PlantSpeciesRecord,
  PlantIdentificationResult,
  PlantCategoryCount,
  PlantAutocompleteItem
} from '../types';

export const IndianPlantExplorer: React.FC = () => {
  // Navigation tabs
  const [activeTab, setActiveTab] = useState<'identify' | 'search'>('identify');

  // Mode A / B Toggle
  const [identifyMode, setIdentifyMode] = useState<'automatic' | 'named'>('automatic');
  const [selectedOrgan, setSelectedOrgan] = useState<string>('leaf');
  const [userPlantName, setUserPlantName] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Autocomplete suggestions for Mode B & Directory Search
  const [modeBSuggestions, setModeBSuggestions] = useState<PlantAutocompleteItem[]>([]);
  const [showModeBAutocomplete, setShowModeBAutocomplete] = useState<boolean>(false);
  const [dirSuggestions, setDirSuggestions] = useState<PlantAutocompleteItem[]>([]);
  const [showDirAutocomplete, setShowDirAutocomplete] = useState<boolean>(false);

  // Identification State
  const [identifying, setIdentifying] = useState<boolean>(false);
  const [idResult, setIdResult] = useState<PlantIdentificationResult | null>(null);
  const [idError, setIdError] = useState<string | null>(null);

  // Directory / Search State
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [categories, setCategories] = useState<PlantCategoryCount[]>([]);
  const [searchResults, setSearchResults] = useState<PlantSummaryItem[]>([]);
  const [totalPlants, setTotalPlants] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [loadingSearch, setLoadingSearch] = useState<boolean>(false);

  // Modal Plant Details
  const [modalPlantId, setModalPlantId] = useState<string | null>(null);
  const [modalPlantDetails, setModalPlantDetails] = useState<PlantSpeciesRecord | null>(null);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [detailTab, setDetailTab] = useState<'overview' | 'botany' | 'care' | 'pests' | 'uses'>('overview');

  // Load initial catalog stats and categories
  useEffect(() => {
    plantService.getCategories().then((cats) => setCategories(cats)).catch(() => {});
    loadDirectory(1, '', '');
  }, []);

  const loadDirectory = async (page: number, q: string, cat: string) => {
    setLoadingSearch(true);
    try {
      const data = await plantService.searchPlants(q, cat, undefined, page, 18);
      setSearchResults(data.items);
      setTotalPlants(data.total);
      setCurrentPage(data.page);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingSearch(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadDirectory(1, searchQuery, selectedCategory);
  };

  const handleCategorySelect = (cat: string) => {
    const newCat = selectedCategory === cat ? '' : cat;
    setSelectedCategory(newCat);
    loadDirectory(1, searchQuery, newCat);
  };

  // Image Selection Handler
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setIdResult(null);
      setIdError(null);
    }
    e.target.value = '';
  };

  // Mode B Autocomplete
  const handlePlantNameType = async (val: string) => {
    setUserPlantName(val);
    if (val.trim().length >= 1) {
      try {
        const items = await plantService.autocompletePlants(val.trim(), 8);
        setModeBSuggestions(items);
        setShowModeBAutocomplete(true);
      } catch {
        setModeBSuggestions([]);
      }
    } else {
      setShowModeBAutocomplete(false);
    }
  };

  const handleSelectModeB = (item: PlantAutocompleteItem) => {
    setUserPlantName(item.commonName);
    setShowModeBAutocomplete(false);
  };

  // Directory Search Autocomplete
  const handleDirectorySearchType = async (val: string) => {
    setSearchQuery(val);
    if (val.trim().length >= 1) {
      try {
        const items = await plantService.autocompletePlants(val.trim(), 8);
        setDirSuggestions(items);
        setShowDirAutocomplete(true);
      } catch {
        setDirSuggestions([]);
      }
    } else {
      setDirSuggestions([]);
      setShowDirAutocomplete(false);
    }
  };

  const handleSelectDirItem = (item: PlantAutocompleteItem) => {
    setSearchQuery(item.commonName);
    setShowDirAutocomplete(false);
    loadDirectory(1, item.commonName, selectedCategory);
  };

  // Run Identification
  const handleIdentify = async () => {
    if (!selectedFile) {
      setIdError('Please select or capture a plant image to identify.');
      return;
    }

    setIdentifying(true);
    setIdError(null);
    setIdResult(null);

    try {
      const result = await plantService.identifyPlant(
        selectedFile,
        identifyMode === 'named' ? userPlantName : undefined,
        selectedOrgan
      );
      setIdResult(result);
    } catch (err: any) {
      setIdError(err.response?.data?.detail || err.message || 'Plant identification failed.');
    } finally {
      setIdentifying(false);
    }
  };

  // View Plant Details in Modal
  const openPlantDetailsModal = async (plantId: string) => {
    setModalPlantId(plantId);
    setLoadingDetails(true);
    setDetailTab('overview');
    try {
      const details = await plantService.getPlantDetails(plantId);
      setModalPlantDetails(details);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingDetails(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fbfcf9] text-gray-900 pb-20">
      {/* Hero Header */}
      <div className="bg-gradient-to-b from-agro-950 via-agro-900 to-agro-850 text-white pt-10 pb-16 px-4 sm:px-6 lg:px-8 border-b border-agro-800">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/30 text-emerald-300 text-xs font-bold uppercase tracking-wider mb-3">
                <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                Plant Vision & Health System
              </div>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white">
                Plant Analysis <span className="text-emerald-400">& Identification</span>
              </h1>
              <p className="mt-3 text-base sm:text-lg text-emerald-100/80 max-w-3xl leading-relaxed">
                Search the botanical directory for many Indian species, or screen a clear leaf / whole-plant photo against the 14 supported image classes. Image accuracy has not been independently verified on real field photographs; unsupported species and plant parts may be inconclusive.
              </p>
            </div>

            {/* Quick Stat Badges */}
            <div className="flex flex-wrap md:flex-col gap-2.5 sm:gap-3 bg-white/5 border border-white/10 backdrop-blur-md rounded-2xl p-4 text-xs font-medium">
              <div className="flex items-center gap-2 text-emerald-200">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>10,208 Botanical Directory Records</span>
              </div>
              <div className="flex items-center gap-2 text-emerald-200">
                <Languages className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Telugu, Tamil, & Hindi Vernacular</span>
              </div>
              <div className="flex items-center gap-2 text-emerald-200">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Local plant directory • Optional AI provider</span>
              </div>
            </div>
          </div>

          {/* Main Module Tabs (2 Clean Tabs) */}
          <div className="flex items-center gap-2 mt-8 border-b border-white/10 pb-1 overflow-x-auto">
            <button
              onClick={() => setActiveTab('identify')}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-sm transition-all whitespace-nowrap ${
                activeTab === 'identify'
                  ? 'bg-emerald-500 text-agro-950 shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              <Camera className="w-4 h-4" />
              Plant Identification & Care
            </button>
            <button
              onClick={() => setActiveTab('search')}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-sm transition-all whitespace-nowrap ${
                activeTab === 'search'
                  ? 'bg-emerald-500 text-agro-950 shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              <Search className="w-4 h-4" />
              Plant Directory & Catalog ({totalPlants})
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        {/* ============================================================== */}
        {/* TAB 1: VISUAL IDENTIFICATION                                   */}
        {/* ============================================================== */}
        {activeTab === 'identify' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Left Control Column */}
            <div className="lg:col-span-5 flex flex-col gap-6">
              <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
                <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
                  <Camera className="w-5 h-5 text-emerald-600" />
                  Capture or Upload Photo
                </h2>
                <p className="text-xs text-gray-700 font-medium mb-4">
                  For image classification, use a clear leaf or whole-plant photo from one of the supported crop classes. Other plant parts are not supported by the vision model.
                </p>

                {/* Mode Selector */}
                <div className="grid grid-cols-2 gap-2 p-1 bg-gray-100 rounded-xl mb-4 text-xs font-bold">
                  <button
                    type="button"
                    onClick={() => {
                      setIdentifyMode('automatic');
                      setUserPlantName('');
                    }}
                    className={`py-2 px-3 rounded-lg transition-all ${
                      identifyMode === 'automatic'
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Mode A: Automatic
                  </button>
                  <button
                    type="button"
                    onClick={() => setIdentifyMode('named')}
                    className={`py-2 px-3 rounded-lg transition-all ${
                      identifyMode === 'named'
                        ? 'bg-white text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Mode B: By Plant Name
                  </button>
                </div>

                {/* Organ Selector */}
                <div className="mb-4">
                  <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                    Plant Part Photographed:
                  </label>
                  <div className="flex flex-wrap gap-1.5">
                    {[
                      { id: 'leaf', label: 'Leaf' },
                      { id: 'flower', label: 'Flower' },
                      { id: 'fruit', label: 'Fruit' },
                      { id: 'stem', label: 'Stem' },
                      { id: 'root', label: 'Root' },
                      { id: 'whole_plant', label: 'Whole Plant' },
                    ].map((org) => (
                      <button
                        key={org.id}
                        type="button"
                        onClick={() => setSelectedOrgan(org.id)}
                        className={`text-xs px-3 py-1.5 rounded-lg border font-semibold transition-all ${
                          selectedOrgan === org.id
                            ? 'bg-emerald-50 border-emerald-500 text-emerald-900 ring-1 ring-emerald-500'
                            : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        {org.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Mode B: Searchable Plant Name Input */}
                {identifyMode === 'named' && (
                  <div className="mb-4 relative">
                    <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                      Enter Plant Name (e.g. Mango, Rice, Neem, Tomato):
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        value={userPlantName}
                        onChange={(e) => handlePlantNameType(e.target.value)}
                        placeholder="Type English, Hindi, Telugu, or Scientific name..."
                        className="w-full pl-9 pr-4 py-2 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                      />
                      <Search className="w-4 h-4 text-gray-500 absolute left-3 top-2.5" />
                    </div>

                    {/* Autocomplete dropdown */}
                    {showModeBAutocomplete && modeBSuggestions.length > 0 && (
                      <div className="absolute z-20 left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-xl max-h-56 overflow-y-auto divide-y divide-gray-100 animate-in fade-in duration-150">
                        {modeBSuggestions.map((item) => (
                          <div
                            key={item.id}
                            className="px-3.5 py-2.5 hover:bg-emerald-50/70 cursor-pointer flex items-center justify-between gap-2"
                            onClick={() => handleSelectModeB(item)}
                          >
                            <div className="min-w-0 flex-1">
                              <span className="text-xs font-bold text-gray-900 block truncate">
                                {item.commonName}
                              </span>
                              <span className="text-[10px] text-emerald-700 italic block truncate">
                                {item.scientificName} {item.hindiName ? `• ${item.hindiName}` : ''} {item.teluguName ? `• ${item.teluguName}` : ''}
                              </span>
                            </div>
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                setShowModeBAutocomplete(false);
                                openPlantDetailsModal(item.id);
                              }}
                              className="shrink-0 px-2 py-1 rounded-md bg-emerald-50 hover:bg-emerald-600 text-emerald-700 hover:text-white text-[10px] font-bold border border-emerald-200 transition-colors flex items-center gap-1"
                              title="Inspect botanical profile"
                            >
                              <BookOpen className="w-3 h-3" />
                              Profile
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Upload Box */}
                <div className="border-2 border-dashed border-gray-300 rounded-2xl p-4 text-center hover:border-emerald-500 transition-colors">
                  {previewUrl ? (
                    <div className="relative rounded-xl overflow-hidden max-h-64 flex justify-center bg-black/5">
                      <img src={previewUrl} alt="Preview" className="max-h-64 object-contain rounded-xl" />
                      <button
                        type="button"
                        onClick={() => {
                          setSelectedFile(null);
                          setPreviewUrl(null);
                          setIdResult(null);
                          setIdError(null);
                        }}
                        className="absolute top-2 right-2 p-1.5 rounded-full bg-black/60 text-white hover:bg-black/80"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ) : (
                    <label className="flex flex-col items-center justify-center cursor-pointer py-8">
                      <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-2">
                        <Upload className="w-6 h-6" />
                      </div>
                      <span className="text-sm font-bold text-gray-800">Click to upload photo</span>
                      <span className="text-xs text-gray-600 mt-1">JPEG, PNG, or WebP up to 15MB</span>
                      <input
                        type="file"
                        accept="image/jpeg,image/png,image/webp"
                        onChange={handleFileChange}
                        className="hidden"
                      />
                    </label>
                  )}
                </div>

                {/* Error Banner */}
                {idError && (
                  <div className="mt-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-red-500" />
                    <span>{idError}</span>
                  </div>
                )}

                {/* Action Button */}
                <button
                  type="button"
                  onClick={handleIdentify}
                  disabled={identifying || !selectedFile}
                  className={`w-full mt-5 py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 shadow-md transition-all ${
                    identifying || !selectedFile
                      ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                      : 'bg-emerald-600 hover:bg-emerald-700 text-white'
                  }`}
                >
                  {identifying ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Analyzing Indian Flora...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      Identify Plant Species
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Right Results Column */}
            <div className="lg:col-span-7 flex flex-col gap-6">
              {idResult ? (
                <div className="flex flex-col gap-6 animate-in fade-in duration-300">
                  <PersistenceNotice savedToAccount={idResult.savedToAccount} message={idResult.persistenceMessage} />
                  {/* Trained Model Organ Capability Honesty Notice */}
                  {idResult.organHonestyNotice && (
                    <div className="p-3.5 rounded-2xl bg-blue-50/70 border border-blue-200 text-blue-900 text-xs flex items-start gap-2.5">
                      <ShieldCheck className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                      <div>
                        <span className="font-bold text-xs uppercase tracking-wider block text-blue-950 mb-0.5">
                          Trained Model Organ Scope:
                        </span>
                        <p className="text-blue-900 leading-relaxed">{idResult.organHonestyNotice}</p>
                      </div>
                    </div>
                  )}

                  {/* Ambiguity Alert if Model is Uncertain or Out-of-Distribution */}
                  {(idResult.isAmbiguous || idResult.inDistribution === false) && (
                    <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                      <div className="flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                        <div>
                          <span className="font-bold block text-sm mb-1">Image and Plant-Part Check</span>
                          <p className="leading-relaxed">{idResult.ambiguityMessage || 'The vision model cannot confirm this specimen with high certainty. It may be an un-modeled species or unsupported organ.'}</p>
                        </div>
                      </div>
                      <button
                        type="button"
                        onClick={() => {
                          const q = idResult.directorySearchQuery || (idResult.topCandidate ? idResult.topCandidate.commonName : '');
                          setActiveTab('search');
                          setSearchQuery(q);
                          loadDirectory(1, q, '');
                        }}
                        className="px-3.5 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs whitespace-nowrap shadow-sm transition-all flex items-center gap-1.5 shrink-0"
                      >
                        <Search className="w-3.5 h-3.5" />
                        Search Plant Directory
                      </button>
                    </div>
                  )}

                  {/* Suggested Matches from 10,000+ Botanical Directory if Ambiguous */}
                  {idResult.suggestedDirectoryMatches && idResult.suggestedDirectoryMatches.length > 0 && (
                    <div className="bg-white rounded-2xl border border-amber-200 p-5 shadow-sm">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <BookOpen className="w-4 h-4 text-amber-600" />
                          <h4 className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                            Suggested Matches from the Plant Directory:
                          </h4>
                        </div>
                        <span className="text-[11px] text-gray-500 font-medium">
                          Non-vision taxonomy catalog lookup
                        </span>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                        {idResult.suggestedDirectoryMatches.map((sMatch) => (
                          <div
                            key={sMatch.id}
                            onClick={() => openPlantDetailsModal(sMatch.id)}
                            className="p-3 rounded-xl border border-gray-100 hover:border-amber-400 hover:bg-amber-50/30 transition-all cursor-pointer flex items-center justify-between group"
                          >
                            <div className="truncate pr-2">
                              <span className="font-bold text-xs text-gray-900 block truncate group-hover:text-amber-700">
                                {sMatch.commonName}
                              </span>
                              <span className="text-[10px] text-gray-500 italic block truncate">
                                {sMatch.scientificName} {sMatch.hindiName ? `• ${sMatch.hindiName}` : ''}
                              </span>
                            </div>
                            <span className="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-md bg-amber-100 text-amber-900">
                              View Profile
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Mode B: User-Selected Target Plant (Manual Input) */}
                  {idResult.targetedPlant && (
                    <div className="bg-slate-50 rounded-2xl border border-slate-200 p-4 text-xs">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="font-bold text-gray-700 uppercase tracking-wider text-[10px] flex items-center gap-1.5">
                          <User className="w-3.5 h-3.5 text-slate-500" />
                          User-Selected Target Plant:
                        </span>
                        <span className="px-2 py-0.5 rounded-full bg-slate-200 text-slate-700 font-bold text-[10px]">
                          Manual Name Input (Not Image-Verified)
                        </span>
                      </div>
                      <div className="text-base font-extrabold text-gray-900">
                        {idResult.targetedPlant.commonName || (idResult.targetedPlant as any).common_name}{' '}
                        <span className="text-xs font-semibold italic text-emerald-800">
                          ({idResult.targetedPlant.scientificName || (idResult.targetedPlant as any).scientific_name})
                        </span>
                      </div>
                    </div>
                  )}

                  {/* Mode B: Morphological Consistency Notice */}
                  {idResult.nameAssistedAnalysis && (
                    <div className={`p-4 rounded-2xl border text-xs flex items-start gap-3 ${
                      idResult.nameAssistedAnalysis.isConsistent
                        ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                        : 'bg-rose-50 border-rose-200 text-rose-900'
                    }`}>
                      {idResult.nameAssistedAnalysis.isConsistent === true ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                      ) : (idResult.nameAssistedAnalysis.isConsistent === false ? (
                        <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
                      ) : (
                        <AlertCircle className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
                      ))}
                      <div>
                        <span className="font-bold text-sm block mb-1">
                          Cross-Check: {idResult.nameAssistedAnalysis.status}
                        </span>
                        <p className="leading-relaxed">{idResult.nameAssistedAnalysis.explanation}</p>
                      </div>
                    </div>
                  )}

                  {/* Top Candidate Hero Card */}
                  {idResult.topCandidate && (
                    <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
                      <div className="flex items-start justify-between gap-4 border-b border-gray-100 pb-4">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-900 capitalize">
                              {idResult.topCandidate.category || 'Plant'}
                            </span>
                            <span className="text-xs text-gray-700 font-semibold">
                              {idResult.analysisSource === 'ollama_vision_screening_unvalidated'
                                ? 'Visual candidate from this photo'
                                : (idResult.isAmbiguous ? 'Unverified model candidate' : '14-class model candidate (real-photo accuracy unverified)')}
                            </span>
                          </div>
                          <h3 className="text-2xl font-extrabold text-gray-900">
                            {idResult.topCandidate.commonName}
                          </h3>
                          <p className="text-sm font-semibold italic text-emerald-700">
                            {idResult.topCandidate.scientificName} • Family: {idResult.topCandidate.family}
                          </p>
                        </div>

                        {/* Confidence Percentage Meter */}
                        <div className="text-right">
                          <span className={`text-2xl font-black ${
                            idResult.isAmbiguous ? 'text-amber-600' : 'text-emerald-600'
                          }`}>
                            {idResult.analysisSource === 'ollama_vision_screening_unvalidated' ? 'Visual match' : `${idResult.topCandidate.confidencePercentage ?? 0}%`}
                          </span>
                          <span className="text-[10px] text-gray-600 block uppercase font-bold tracking-wider">
                            {idResult.analysisSource === 'ollama_vision_screening_unvalidated' ? 'Image-based candidate' : 'Estimated model score'}
                          </span>
                        </div>
                      </div>

                      {/* Regional Names Badge Row */}
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 my-4 p-3 bg-gray-50 rounded-xl text-xs">
                        {idResult.topCandidate.hindiName && (
                          <div>
                            <span className="text-gray-600 block font-bold text-[10px] uppercase">Hindi</span>
                            <span className="font-bold text-gray-900">{idResult.topCandidate.hindiName}</span>
                          </div>
                        )}
                        {idResult.topCandidate.teluguName && (
                          <div>
                            <span className="text-gray-600 block font-bold text-[10px] uppercase">Telugu</span>
                            <span className="font-bold text-gray-900">{idResult.topCandidate.teluguName}</span>
                          </div>
                        )}
                        {idResult.topCandidate.tamilName && (
                          <div>
                            <span className="text-gray-600 block font-bold text-[10px] uppercase">Tamil</span>
                            <span className="font-bold text-gray-900">{idResult.topCandidate.tamilName}</span>
                          </div>
                        )}
                      </div>

                      {/* Detected Plant Part / Organ Badge */}
                      {idResult.organAnalysis && (
                        <div className="my-3 p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-gray-700 uppercase tracking-wider text-[10px]">Plant Part Photographed:</span>
                            <span className="px-2.5 py-0.5 rounded-full bg-emerald-600 text-white font-bold capitalize text-xs shadow-sm">
                              {idResult.organAnalysis.organ.replace('_', ' ')}
                            </span>
                          </div>
                          <span className="text-[11px] text-emerald-800 font-medium">{idResult.organAnalysis.evidence}</span>
                        </div>
                      )}

                      {/* Visual Botanical Evidence Badges */}
                      {idResult.visualEvidence && idResult.visualEvidence.length > 0 && (
                        <div className="mb-4">
                          <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
                            Observable Visual Features:
                          </h4>
                          <div className="space-y-1.5">
                            {idResult.visualEvidence.map((ev, i) => (
                              <div key={i} className="text-xs text-gray-700 flex items-start gap-2">
                                <Check className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                                <span>{ev}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {(idResult.visualSummary || idResult.visualCondition || idResult.ripenessStatus || idResult.spoilageStatus || idResult.possibleIssues?.length || idResult.precautions?.length) && (
                        <div className="my-4 rounded-2xl border border-emerald-200 bg-emerald-50/50 p-4 space-y-3">
                          <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-950">Image Summary & Visible Condition</h4>
                          {idResult.visualSummary && <p className="text-sm leading-relaxed text-gray-700">{idResult.visualSummary}</p>}
                          <div className="flex flex-wrap gap-2">
                            {idResult.visualCondition && <span className="rounded-full bg-amber-100 px-2.5 py-1 text-[11px] font-semibold text-amber-900">Condition: {idResult.visualCondition.replace(/_/g, ' ')}</span>}
                            {idResult.ripenessStatus && idResult.ripenessStatus !== 'not_applicable' && <span className="rounded-full bg-orange-100 px-2.5 py-1 text-[11px] font-semibold text-orange-900">Ripeness: {idResult.ripenessStatus.replace(/_/g, ' ')}</span>}
                            {idResult.spoilageStatus && idResult.spoilageStatus !== 'not_applicable' && <span className="rounded-full bg-rose-100 px-2.5 py-1 text-[11px] font-semibold text-rose-900">Visible spoilage: {idResult.spoilageStatus.replace(/_/g, ' ')}</span>}
                          </div>
                          {!!idResult.possibleIssues?.length && <div className="space-y-2"><p className="text-[11px] font-bold uppercase tracking-wide text-amber-900">Possible issues — not confirmed</p>{idResult.possibleIssues.map((issue, i) => <div key={i} className="rounded-xl border border-amber-200 bg-amber-50 p-3"><p className="text-xs font-bold text-amber-950">{issue.name || 'Possible visible issue'}</p>{issue.evidence && <p className="mt-1 text-xs text-gray-700">Visible evidence: {issue.evidence}</p>}</div>)}</div>}
                          {!!idResult.precautions?.length && <div><p className="mb-1 text-[11px] font-bold uppercase tracking-wide text-gray-600">Precautions</p><ul className="list-disc space-y-1 pl-5 text-xs text-gray-700">{idResult.precautions.slice(0, 5).map((item, i) => <li key={i}>{item}</li>)}</ul></div>}
                          {idResult.analysisSource === 'ollama_vision_screening_unvalidated' && <p className="border-t border-emerald-100 pt-2 text-[11px] text-gray-600">Use the photo as a visual guide; confirm important plant or disease identification with a trusted botanical or agricultural source.</p>}
                        </div>
                      )}

                      {/* Health & Vitality Condition */}
                      {idResult.healthAssessment && (
                        <div className={`my-4 p-4 rounded-xl border ${idResult.isAmbiguous ? 'bg-amber-50/80 border-amber-200' : 'bg-emerald-50/70 border-emerald-200'}`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className={`text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 ${idResult.isAmbiguous ? 'text-amber-950' : 'text-emerald-950'}`}>
                              <HeartPulse className={`w-4 h-4 ${idResult.isAmbiguous ? 'text-amber-600' : 'text-emerald-600'}`} />
                              Foliar Health Status
                            </span>
                            <span className={`text-xs font-extrabold px-2.5 py-0.5 rounded-full ${idResult.isAmbiguous ? 'bg-amber-200/90 text-amber-950' : 'bg-emerald-200/80 text-emerald-900'}`}>
                              {idResult.healthAssessment.healthStatus}
                              {!idResult.isAmbiguous && idResult.healthAssessment.healthScorePercentage > 0 && ` (${idResult.healthAssessment.healthScorePercentage}%)`}
                            </span>
                          </div>
                          <div className="space-y-1">
                            {idResult.healthAssessment.symptoms.map((sym, sIdx) => (
                              <p key={sIdx} className={`text-xs flex items-start gap-1.5 ${idResult.isAmbiguous ? 'text-amber-900' : 'text-emerald-900'}`}>
                                <span className={`${idResult.isAmbiguous ? 'text-amber-600' : 'text-emerald-500'} font-bold`}>•</span>
                                {sym}
                              </p>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Tailored Care & Growth Suggestions (5 Points) */}
                      {idResult.recommendations && idResult.recommendations.length > 0 && (
                        <div className="my-4 pt-3 border-t border-gray-100">
                          <h4 className="text-xs font-bold text-gray-900 uppercase tracking-wider mb-3 flex items-center gap-2">
                            <Sparkles className={`w-4 h-4 ${idResult.isAmbiguous ? 'text-amber-600' : 'text-emerald-600'}`} />
                            {idResult.isAmbiguous ? 'Safe Handling & General Care Guidance:' : 'Actionable Care & Growth Suggestions:'}
                          </h4>
                          <div className="grid grid-cols-1 gap-2.5">
                            {idResult.recommendations.map((rec, rIdx) => (
                              <div key={rIdx} className={`p-3 rounded-xl border text-xs ${idResult.isAmbiguous ? 'bg-amber-50/40 border-amber-100' : 'bg-gray-50 border-gray-100'}`}>
                                <span className="font-bold text-gray-900 block mb-0.5">{rIdx + 1}. {rec.title}</span>
                                <span className="text-gray-600 leading-relaxed">{rec.description}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* CTA: show catalog details only when there is a real catalog record. */}
                      <div className="pt-3 border-t border-gray-100">
                        {(idResult.topCandidate.id || idResult.topCandidate.plantId) ? (
                          <button
                            type="button"
                            onClick={() => openPlantDetailsModal((idResult.topCandidate!.id || idResult.topCandidate!.plantId)!)}
                            className="w-full py-3 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-sm transition-all"
                          >
                            <BookOpen className="w-4 h-4" />
                            View Complete Botanical Profile & Pests for {idResult.topCandidate.commonName}
                          </button>
                        ) : (
                          <p className="text-xs leading-relaxed text-gray-600 rounded-xl bg-amber-50 border border-amber-200 p-3">
                            This is a visual candidate, not a matched catalogue record. Search the plant catalogue by its common or scientific name to open a verified profile.
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Ranked Candidates (Top 5) */}
                  <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
                    <h4 className="text-sm font-bold text-gray-900 mb-3">
                      Ranked Candidate Species ({idResult.candidates.length})
                    </h4>
                    <div className="space-y-3">
                      {idResult.candidates.map((cand, idx) => (
                        <div
                          key={cand.id || cand.plantId || idx}
                          className="flex items-center justify-between p-3 rounded-xl border border-gray-100 hover:border-emerald-300 hover:bg-emerald-50/30 transition-all text-xs"
                        >
                          <div className="flex items-center gap-3">
                            <span className="w-6 h-6 rounded-full bg-gray-100 text-gray-800 font-bold flex items-center justify-center text-xs">
                              {cand.rank || idx + 1}
                            </span>
                            <div>
                              <span className="font-bold text-gray-900 block text-sm">
                                {cand.commonName || cand.plantId}
                              </span>
                              <span className="text-gray-500 italic">
                                {cand.scientificName || 'Botanical Species'}
                              </span>
                            </div>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="font-bold text-emerald-600">
                              {idResult.analysisSource === 'ollama_vision_screening_unvalidated' ? 'Visual match' : `${cand.confidencePercentage ?? (cand.confidence != null ? Math.round(cand.confidence * 100) : 0)}%`}
                            </span>
                            {(cand.id || cand.plantId) ? (
                              <button
                                type="button"
                                onClick={() => openPlantDetailsModal((cand.id || cand.plantId)!)}
                                className="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-900"
                                title="View details"
                              >
                                <ChevronRight className="w-4 h-4" />
                              </button>
                            ) : (
                              <span className="text-[10px] text-gray-500">No catalogue match</span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                /* Empty state guide */
                <div className="bg-white rounded-2xl border border-gray-200 p-8 text-center flex flex-col items-center justify-center min-h-[360px]">
                  <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                    <Sprout className="w-8 h-8" />
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">
                    Awaiting Plant Photograph
                  </h3>
                  <p className="text-xs text-gray-700 max-w-md leading-relaxed font-medium">
                    Upload or capture a clear photo of an Indian crop, fruit tree, Ayurvedic herb, or garden plant. AGRO AI will evaluate top species candidates, display regional names, and analyze foliar health.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ============================================================== */}
        {/* TAB 2: PLANT DIRECTORY & SEARCH                                */}
        {/* ============================================================== */}
        {activeTab === 'search' && (
          <div className="flex flex-col gap-6">
            {/* Search Input & Filters */}
            <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
              <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3 relative">
                <div className="relative flex-1">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => handleDirectorySearchType(e.target.value)}
                    onFocus={() => { if (dirSuggestions.length > 0) setShowDirAutocomplete(true); }}
                    placeholder="Search plants: common name, scientific name, Telugu, Tamil, or Hindi..."
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                  <Search className="w-5 h-5 text-gray-400 absolute left-3 top-3.5" />

                  {/* Google-Style Instant Autocomplete Dropdown */}
                  {showDirAutocomplete && dirSuggestions.length > 0 && (
                    <div className="absolute z-30 left-0 right-0 mt-1.5 bg-white border border-gray-200 rounded-2xl shadow-2xl max-h-80 overflow-y-auto divide-y divide-gray-100 animate-in fade-in slide-in-from-top-1 duration-150">
                      <div className="px-3.5 py-2 bg-gray-50 flex items-center justify-between text-[11px] text-gray-700 font-semibold border-b border-gray-100">
                        <span className="flex items-center gap-1.5 text-emerald-800">
                          <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
                          Botanical Autocomplete Suggestions ({dirSuggestions.length})
                        </span>
                        <button
                          type="button"
                          onClick={() => setShowDirAutocomplete(false)}
                          className="hover:text-gray-900 text-gray-500"
                        >
                          <X className="w-3.5 h-3.5" />
                        </button>
                      </div>
                      {dirSuggestions.map((item) => (
                        <div
                          key={item.id}
                          className="px-4 py-2.5 hover:bg-emerald-50/70 transition-colors flex items-center justify-between gap-3 group cursor-pointer"
                          onClick={() => handleSelectDirItem(item)}
                        >
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-gray-900 truncate group-hover:text-emerald-900">
                                {item.commonName}
                              </span>
                              <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-gray-100 text-gray-700">
                                {item.category}
                              </span>
                              {item.matchSource !== 'common' && (
                                <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">
                                  Matched: {item.matchSource}
                                </span>
                              )}
                            </div>
                            <div className="text-[11px] text-emerald-700 italic truncate mt-0.5">
                              {item.scientificName} • Family: {item.family}
                            </div>
                            {(item.teluguName || item.hindiName || item.tamilName) && (
                              <div className="text-[10px] text-gray-700 flex items-center gap-3 mt-0.5">
                                {item.teluguName && <span><b className="text-gray-800">TE:</b> {item.teluguName}</span>}
                                {item.hindiName && <span><b className="text-gray-800">HI:</b> {item.hindiName}</span>}
                                {item.tamilName && <span><b className="text-gray-800">TA:</b> {item.tamilName}</span>}
                              </div>
                            )}
                          </div>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              setShowDirAutocomplete(false);
                              openPlantDetailsModal(item.id);
                            }}
                            className="shrink-0 px-2.5 py-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-600 text-emerald-700 hover:text-white text-xs font-bold transition-all flex items-center gap-1 border border-emerald-200 hover:border-emerald-600 shadow-sm"
                            title="Open full botanical record"
                          >
                            <BookOpen className="w-3.5 h-3.5" />
                            <span>Details</span>
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <button
                  type="submit"
                  className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-sm transition-all shrink-0"
                >
                  Search Catalog
                </button>
              </form>

              {/* Category Pills */}
              {categories.length > 0 && (
                <div className="flex items-center gap-2 mt-4 pt-4 border-t border-gray-100 overflow-x-auto pb-1">
                  <span className="text-xs font-bold text-gray-500 uppercase tracking-wider shrink-0 mr-1 flex items-center gap-1">
                    <Filter className="w-3.5 h-3.5" />
                    Categories:
                  </span>
                  {categories.map((c) => (
                    <button
                      key={c.category}
                      type="button"
                      onClick={() => handleCategorySelect(c.category)}
                      className={`text-xs px-3 py-1.5 rounded-lg font-semibold shrink-0 transition-all capitalize ${
                        selectedCategory === c.category
                          ? 'bg-emerald-600 text-white shadow-sm'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {c.category} ({c.count})
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Plants Grid */}
            {loadingSearch ? (
              <div className="py-20 flex justify-center items-center">
                <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
              </div>
            ) : searchResults.length > 0 ? (
              <div className="flex flex-col gap-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {searchResults.map((plant) => (
                    <div
                      key={plant.id}
                      className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm hover:shadow-md hover:border-emerald-300 transition-all flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-900 capitalize">
                            {plant.category}
                          </span>
                          <span className="text-[10px] text-gray-600 font-semibold capitalize">
                            {plant.statusInIndia}
                          </span>
                        </div>
                        <h4 className="font-bold text-base text-gray-900 leading-snug">
                          {plant.commonName}
                        </h4>
                        <p className="text-xs italic font-semibold text-emerald-700 mt-0.5">
                          {plant.scientificName}
                        </p>
                        <p className="text-[11px] text-gray-600 mt-1">
                          Family: {plant.family}
                        </p>

                        {/* Regional Names snippet */}
                        <div className="mt-3 pt-2.5 border-t border-gray-100 text-[11px] text-gray-600 space-y-0.5">
                          {plant.hindiName && (
                            <div><span className="font-bold text-gray-700">HI:</span> {plant.hindiName}</div>
                          )}
                          {plant.teluguName && (
                            <div><span className="font-bold text-gray-700">TE:</span> {plant.teluguName}</div>
                          )}
                          {plant.tamilName && (
                            <div><span className="font-bold text-gray-700">TA:</span> {plant.tamilName}</div>
                          )}
                        </div>
                      </div>

                      <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between gap-2">
                        <button
                          type="button"
                          onClick={() => openPlantDetailsModal(plant.id)}
                          className="flex-1 py-1.5 px-3 rounded-lg bg-gray-50 hover:bg-emerald-50 text-emerald-800 font-bold text-xs flex items-center justify-center gap-1 transition-all"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          Details
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setActiveTab('identify');
                            setIdentifyMode('named');
                            setUserPlantName(plant.commonName);
                            window.scrollTo({ top: 250, behavior: 'smooth' });
                          }}
                          className="py-1.5 px-3 rounded-lg border border-emerald-300 hover:bg-emerald-50 text-emerald-800 font-bold text-xs flex items-center gap-1"
                          title="Identify or verify this plant"
                        >
                          <Camera className="w-3.5 h-3.5" />
                          Identify
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Pagination Controls */}
                {totalPlants > 18 && (
                  <div className="flex items-center justify-between p-4 bg-white rounded-2xl border border-gray-200 mt-2">
                    <span className="text-xs text-gray-600 font-medium">
                      Showing Page {currentPage} of {Math.max(1, Math.ceil(totalPlants / 18))} ({totalPlants} Total Species)
                    </span>
                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => loadDirectory(currentPage - 1, searchQuery, selectedCategory)}
                        disabled={currentPage <= 1 || loadingSearch}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold ${
                          currentPage <= 1
                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                            : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                        }`}
                      >
                        Previous
                      </button>
                      <button
                        type="button"
                        onClick={() => loadDirectory(currentPage + 1, searchQuery, selectedCategory)}
                        disabled={currentPage * 18 >= totalPlants || loadingSearch}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold ${
                          currentPage * 18 >= totalPlants
                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                            : 'bg-emerald-600 text-white hover:bg-emerald-700'
                        }`}
                      >
                        Next
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-white rounded-2xl border border-gray-200 p-12 text-center">
                <Search className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <h4 className="font-bold text-gray-900 text-base">No Matching Species Found</h4>
                <p className="text-xs text-gray-500 mt-1">
                  Try searching with alternative spellings or clear category filters.
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* ============================================================== */}
      {/* MODAL: FULL BOTANICAL PLANT DETAILS VIEW                       */}
      {/* ============================================================== */}
      {modalPlantId && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-3xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-gray-100 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            {/* Modal Header */}
            <div className="p-6 bg-gradient-to-r from-agro-950 to-agro-900 text-white flex items-start justify-between">
              <div>
                <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 uppercase tracking-wider">
                  {modalPlantDetails?.category || 'Indian Botanical Record'}
                </span>
                <h3 className="text-2xl font-black mt-1">
                  {modalPlantDetails?.commonName || 'Plant Profile'}
                </h3>
                <p className="text-xs text-emerald-200 italic font-medium">
                  {modalPlantDetails?.scientificName} • Family: {modalPlantDetails?.family}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setModalPlantId(null)}
                className="p-2 rounded-full hover:bg-white/10 text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Sub-tabs in Modal */}
            <div className="flex border-b border-gray-200 bg-gray-50 px-6 gap-2 overflow-x-auto text-xs font-bold">
              {[
                { id: 'overview', label: 'Overview & Names' },
                { id: 'botany', label: 'Botanical Traits' },
                { id: 'care', label: 'Care & Cultivation' },
                { id: 'pests', label: 'Pests & Diseases' },
                { id: 'uses', label: 'Uses & Safety' },
              ].map((t) => (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => setDetailTab(t.id as any)}
                  className={`py-3 px-3 border-b-2 font-bold whitespace-nowrap transition-colors ${
                    detailTab === t.id
                      ? 'border-emerald-600 text-emerald-800 bg-white'
                      : 'border-transparent text-gray-500 hover:text-gray-800'
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto flex-1 text-xs text-gray-700 space-y-4">
              {loadingDetails ? (
                <div className="py-16 flex justify-center">
                  <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
                </div>
              ) : modalPlantDetails ? (
                <>
                  {/* OVERVIEW TAB */}
                  {detailTab === 'overview' && (
                    <div className="space-y-4">
                      {/* Regional Names Grid */}
                      <div className="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-100">
                        <h4 className="font-bold text-emerald-950 uppercase tracking-wider text-[11px] mb-2 flex items-center gap-1.5">
                          <Languages className="w-4 h-4 text-emerald-600" />
                          Indian Vernacular & Regional Names:
                        </h4>
                        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                          <div>
                            <span className="font-bold text-gray-500 text-[10px] block">Hindi (हिन्दी)</span>
                            <span className="font-bold text-gray-900">{modalPlantDetails.hindiName || 'N/A'}</span>
                          </div>
                          <div>
                            <span className="font-bold text-gray-500 text-[10px] block">Telugu (తెలుగు)</span>
                            <span className="font-bold text-gray-900">{modalPlantDetails.teluguName || 'N/A'}</span>
                          </div>
                          <div>
                            <span className="font-bold text-gray-500 text-[10px] block">Tamil (தமிழ்)</span>
                            <span className="font-bold text-gray-900">{modalPlantDetails.tamilName || 'N/A'}</span>
                          </div>
                          {Object.entries(modalPlantDetails.otherRegionalNames || {}).map(([lang, name]) => (
                            <div key={lang}>
                              <span className="font-bold text-gray-500 text-[10px] block capitalize">{lang}</span>
                              <span className="font-bold text-gray-900">{name}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Distribution & Habitat */}
                      <div>
                        <h4 className="font-bold text-gray-900 mb-1">Distribution in India:</h4>
                        <p className="text-gray-600">
                          {modalPlantDetails.indianStates?.join(', ') || 'Documented pan-India.'}
                        </p>
                      </div>

                      <div>
                        <h4 className="font-bold text-gray-900 mb-1">Habitat & Climate Niche:</h4>
                        <p className="text-gray-600">{modalPlantDetails.habitatAndClimate || 'Tropical and subtropical India.'}</p>
                      </div>
                    </div>
                  )}

                  {/* BOTANY TAB */}
                  {detailTab === 'botany' && (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div className="p-3 bg-gray-50 rounded-xl">
                          <span className="font-bold text-gray-900 block mb-1">Leaf Morphology</span>
                          <ul className="space-y-1 text-gray-600">
                            <li>• Shape: {modalPlantDetails.leafCharacteristics?.shape || 'Standard'}</li>
                            <li>• Margin: {modalPlantDetails.leafCharacteristics?.margin || 'Entire'}</li>
                            <li>• Venation: {modalPlantDetails.leafCharacteristics?.venation || 'Pinnate'}</li>
                            <li>• Color: {modalPlantDetails.leafCharacteristics?.color || 'Green'}</li>
                          </ul>
                        </div>
                        <div className="p-3 bg-gray-50 rounded-xl">
                          <span className="font-bold text-gray-900 block mb-1">Stem & Habit</span>
                          <p className="text-gray-600">{modalPlantDetails.stemCharacteristics || modalPlantDetails.growthHabit}</p>
                        </div>
                      </div>

                      {modalPlantDetails.flowerCharacteristics && (
                        <div>
                          <h4 className="font-bold text-gray-900 mb-1">Flowers & Inflorescence:</h4>
                          <p className="text-gray-600">{modalPlantDetails.flowerCharacteristics}</p>
                        </div>
                      )}

                      {modalPlantDetails.fruitCharacteristics && (
                        <div>
                          <h4 className="font-bold text-gray-900 mb-1">Fruit & Seed Characteristics:</h4>
                          <p className="text-gray-600">{modalPlantDetails.fruitCharacteristics}</p>
                        </div>
                      )}
                    </div>
                  )}

                  {/* CARE TAB */}
                  {detailTab === 'care' && (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div className="p-3 bg-amber-50/50 rounded-xl border border-amber-100">
                          <span className="font-bold text-amber-950 flex items-center gap-1.5 mb-1">
                            <Sun className="w-3.5 h-3.5 text-amber-600" />
                            Sunlight
                          </span>
                          <p className="text-gray-700">{modalPlantDetails.sunlightRequirements}</p>
                        </div>

                        <div className="p-3 bg-blue-50/50 rounded-xl border border-blue-100">
                          <span className="font-bold text-blue-950 flex items-center gap-1.5 mb-1">
                            <Droplets className="w-3.5 h-3.5 text-blue-600" />
                            Watering
                          </span>
                          <p className="text-gray-700">{modalPlantDetails.waterRequirements}</p>
                        </div>
                      </div>

                      <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100 flex items-start justify-between gap-3">
                        <div>
                          <span className="font-bold text-emerald-950 flex items-center gap-1.5 mb-1">
                            <Layers className="w-3.5 h-3.5 text-emerald-600" />
                            Soil Preferences:
                          </span>
                          <p className="text-gray-700">{modalPlantDetails.soilPreferences}</p>
                        </div>
                        <Link
                          to="/production/soil"
                          className="shrink-0 text-[11px] font-bold text-emerald-700 hover:text-emerald-900 underline flex items-center gap-1"
                        >
                          Test Soil <ExternalLink className="w-3 h-3" />
                        </Link>
                      </div>

                      <div>
                        <h4 className="font-bold text-gray-900 mb-1">Growing Season & Propagation:</h4>
                        <p className="text-gray-600 mb-1">• Season: {modalPlantDetails.growingSeason}</p>
                        <p className="text-gray-600">• Propagation: {modalPlantDetails.propagationMethods?.join(', ')}</p>
                      </div>
                    </div>
                  )}

                  {/* PESTS TAB */}
                  {detailTab === 'pests' && (
                    <div className="space-y-3">
                      <h4 className="font-bold text-gray-900 mb-2">Common Documented Pathogens & Pests:</h4>
                      {modalPlantDetails.commonPestsAndDiseases && modalPlantDetails.commonPestsAndDiseases.length > 0 ? (
                        modalPlantDetails.commonPestsAndDiseases.map((pst, i) => (
                          <div key={i} className="p-3 rounded-xl border border-gray-100 bg-gray-50">
                            <div className="flex justify-between items-center mb-1">
                              <span className="font-bold text-gray-900">{pst.name}</span>
                              {pst.type && (
                                <span className="text-[10px] uppercase font-bold text-gray-500">
                                  {pst.type}
                                </span>
                              )}
                            </div>
                            {pst.symptoms && <p className="text-gray-600 mb-1">Symptoms: {pst.symptoms}</p>}
                            {pst.management && (
                              <p className="text-emerald-800 font-medium">Control: {pst.management}</p>
                            )}
                          </div>
                        ))
                      ) : (
                        <p className="text-gray-500">No major destructive pathogens recorded.</p>
                      )}
                    </div>
                  )}

                  {/* USES & SAFETY TAB */}
                  {detailTab === 'uses' && (
                    <div className="space-y-4">
                      {/* Toxicity Banner if Toxic */}
                      {modalPlantDetails.isToxic && (
                        <div className="p-3.5 bg-rose-50 border border-rose-200 rounded-xl text-rose-900 flex items-start gap-2.5">
                          <ShieldAlert className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                          <div>
                            <span className="font-bold block mb-0.5 text-xs">Botanical Toxicity Warning:</span>
                            <p>{modalPlantDetails.safetyNotes}</p>
                          </div>
                        </div>
                      )}

                      <div>
                        <h4 className="font-bold text-gray-900 mb-1.5">Documented Traditional & Commercial Uses:</h4>
                        <ul className="space-y-1 text-gray-600">
                          {modalPlantDetails.uses?.map((u, i) => (
                            <li key={i}>• {u}</li>
                          ))}
                        </ul>
                      </div>

                      {/* Sources */}
                      <div className="pt-3 border-t border-gray-100">
                        <span className="font-bold text-gray-500 text-[10px] uppercase block mb-1">
                          Authoritative Sources & Taxa Custodians:
                        </span>
                        <div className="flex flex-wrap gap-2">
                          {modalPlantDetails.sources?.map((s, i) => (
                            <a
                              key={i}
                              href={s.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-[10px] text-emerald-700 hover:underline flex items-center gap-1"
                            >
                              {s.title} <ExternalLink className="w-2.5 h-2.5" />
                            </a>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </>
              ) : null}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
