import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, X, AlertCircle } from 'lucide-react';

interface ImageUploaderProps {
  onImageSelected: (file: File) => void;
  onClearImage?: () => void;
  selectedImage: File | null;
  label?: string;
  helperText?: string;
  accept?: string;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({
  onImageSelected,
  onClearImage,
  selectedImage,
  label = 'Upload Image',
  helperText = 'Supports JPG, JPEG, PNG, WebP up to 15MB',
  accept = 'image/jpeg,image/png,image/webp,image/jpg',
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    setError(null);

    // Validate size (15MB)
    if (file.size > 15 * 1024 * 1024) {
      setError('File is too large. Maximum size is 15MB.');
      return;
    }

    // Validate type
    if (!file.type.startsWith('image/')) {
      setError('Invalid file format. Please upload an image file.');
      return;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    onImageSelected(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleClear = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = '';
    if (onClearImage) onClearImage();
  };

  return (
    <div className="w-full space-y-2">
      {label && <label className="block text-sm font-semibold text-gray-800">{label}</label>}

      {error && (
        <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-xs">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept={accept}
        className="hidden"
        onChange={(e) => {
          if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
          }
          e.target.value = '';
        }}
      />

      {!selectedImage && !previewUrl ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center gap-3 ${
            dragActive
              ? 'border-green-500 bg-green-50/70 scale-[0.99]'
              : 'border-gray-300 hover:border-green-600 hover:bg-green-50/30 bg-white'
          }`}
        >
          <div className="w-14 h-14 rounded-2xl bg-agro-50 text-agro-700 flex items-center justify-center shadow-inner">
            <UploadCloud className="w-7 h-7 text-green-600 animate-pulse" />
          </div>

          <div className="space-y-1">
            <p className="text-sm font-bold text-gray-800">
              Click to upload or drag & drop image
            </p>
            <p className="text-xs text-gray-500">{helperText}</p>
          </div>

          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-gray-100 text-[11px] font-semibold text-gray-600">
            <ImageIcon className="w-3.5 h-3.5" /> High resolution recommended
          </div>
        </div>
      ) : (
        <div className="relative rounded-2xl overflow-hidden border border-gray-200 bg-gray-900 shadow-md group">
          <img
            src={previewUrl || URL.createObjectURL(selectedImage!)}
            alt="Upload preview"
            className="w-full h-64 sm:h-72 object-contain bg-black/60 mx-auto"
          />

          <div className="absolute top-3 right-3 flex items-center gap-2">
            <button
              onClick={handleClear}
              type="button"
              className="p-1.5 bg-black/70 hover:bg-red-600 text-white rounded-full backdrop-blur-md transition-colors shadow-md"
              title="Remove image"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent p-3 text-white flex items-center justify-between">
            <div className="truncate max-w-[70%] text-xs font-medium">
              {selectedImage?.name || 'Selected Image'}
            </div>
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="text-xs font-semibold text-green-400 hover:text-green-300 underline"
            >
              Change Image
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
